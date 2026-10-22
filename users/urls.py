from django.urls import path
from .views import RegisterAPIView, ConfirmUserAPIView, LoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('confirm/', ConfirmUserAPIView.as_view(), name='confirm-user'),
    path('login/', LoginAPIView.as_view(), name='login'),
]