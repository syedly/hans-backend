from django.urls import path
from .views import (
    LoginAPIView, SignupAPIView, 
    PurchaseListAPIView, ProductListAPIView,
    PurchaseStatsView
    )

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('signup/', SignupAPIView.as_view(), name='api-signup'),
    path('purchases/', PurchaseListAPIView.as_view(), name='api-purchases'),
    path('products/', ProductListAPIView.as_view(), name='api-products'),
    # --- barchart and piechart stats endpoint ---
    path("purchase/stats/", PurchaseStatsView.as_view(), name="purchase-stats"),
]
