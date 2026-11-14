"""
URL configuration for caffiestaan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from core.views import CafeConfigAPIView
from accounts.views import AddressViewSet

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='user-address')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('staff/', include('dashboard.urls', namespace='dashboard')),
    path('api/v1/menu/', include('menu.urls', namespace='menu_api')),
    path('', RedirectView.as_view(url='/staff/kds/', permanent=False)),
    path('api/v1/orders/', include('orders.urls', namespace='orders_api')),
    path('api/v1/auth/', include('accounts.urls', namespace='accounts_api')),
    path('api/v1/config/', CafeConfigAPIView.as_view(), name='cafe_config'),
    path('api/v1/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
