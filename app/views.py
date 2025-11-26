from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView
from .serializers import (
    LoginSerializer, SignupSerializer,
    PurchaseSerializer, ProductSerializer
    )
#
from .models import (
    Product, Purchase
    )
#

class SignupAPIView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "email": user.email,
            "username": user.username
        }, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "email": user.email,
            "username": user.username
        }, status=status.HTTP_200_OK)

class PurchaseListAPIView(ListAPIView):
    queryset = Purchase.objects.all().order_by('-id')
    serializer_class = PurchaseSerializer

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer

# bar and pie charts values
from django.db.models import Count, F, Value, CharField
from django.db.models.functions import Concat
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Purchase
from .serializers import PurchaseStatsSerializer

class PurchaseStatsView(GenericAPIView):
    serializer_class = PurchaseStatsSerializer

    def get(self, request, *args, **kwargs):

        # ----------- FULL DATE LIST -----------
        full_dates = (
            Purchase.objects
            .annotate(
                full_date=Concat(
                    F('purchase_year'), Value('-'),
                    F('purchase_month'), Value('-'),
                    F('purchase_date'),
                    output_field=CharField()
                )
            )
            .values_list('full_date', flat=True)
        )

        # ----------- BAR CHART (Month + Year) -----------
        bar_chart = (
            Purchase.objects
            .values('purchase_month', 'purchase_year')
            .annotate(total=Count('id'))
            .order_by('purchase_year', 'purchase_month')
        )

        # ----------- PIE CHART (Province + Year) -----------
        pie_chart = (
            Purchase.objects
            .values('province', 'purchase_year')
            .annotate(total=Count('id'))
            .order_by('province')
        )

        data = {
            "full_dates": list(full_dates),
            "bar_chart": list(bar_chart),
            "pie_chart": list(pie_chart),
        }

        serializer = self.get_serializer(data)
        return Response(serializer.data)
