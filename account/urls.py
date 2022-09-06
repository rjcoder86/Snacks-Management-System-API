from django.urls import path
from .views import RegistrationView, LoginView,validate

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('validate/<uid>/<token>/', validate, name='validate'),
]