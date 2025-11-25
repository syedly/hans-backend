from django.urls import path
from .views import (
    LoginAPIView, SignupAPIView
    )

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('signup/', SignupAPIView.as_view(), name='api-signup'),
]
