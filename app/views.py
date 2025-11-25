from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView
from .models import Purchase
from .serializers import (
    LoginSerializer, SignupSerializer,
    PurchaseSerializer
    )
from .models import (
    CustomUser, Purchase
    )

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
