# accounts/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPIView, MeAPIView
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('me/', MeAPIView.as_view(), name='me'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
]