"""sayaradz_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth.models import User
from sayaradz.models import Manufacturer, ManufacturerUser
from rest_framework import routers
from sayaradz.views import ManufacturerUserList, ManufacturerList, AdminRegistrationAPIView,LogoutView, ManufacturerUserRegistrationAPIView, UserViewSet, ManufacturerViewSet, ManufacturerUserViewSet, AdminLoginAPIView, ManufacturerUserLoginAPIView, TokenAPIView

from rest_framework.authtoken import views as rest_framework_views

from rest_framework.documentation import include_docs_urls 
# Routers provide an easy way of automatically determining the URL conf.

router = routers.DefaultRouter()

#router.register(r'api/users/', UserViewSet)

router.register(r'api/manufacturers', ManufacturerViewSet, base_name='manufacturers')

router.register(r'api/manufacturers-users', ManufacturerUserViewSet)

# Wire up our API using automatic URL routing.

# Additionally, we include login URLs for the browsable API.

urlpatterns = [

    path('admin/', admin.site.urls),    

    path(r'', include(router.urls)),

    path(r'api/', include('rest_framework.urls', namespace='rest_framework')),

    path(r'api/docs', include_docs_urls(title='Sayara DZ API')),

    path(r'api/manufacturers-user-filter', ManufacturerUserList.as_view(), name="filter"),

    path(r'api/manufacturers-filter', ManufacturerList.as_view(), name="filter"),

    path('api/admin/login/', AdminLoginAPIView.as_view(), name="login_admin"),

    path('api/manufacturer-user/login', ManufacturerUserLoginAPIView.as_view(), name="login_manufactureruser"),

    path('api/admin/logout', LogoutView.as_view(), name="logout_admin"),

    path('api/manufacturer-user/logout', LogoutView.as_view(), name="logout_manufactureruser"),

    #path('tokens/<key>/', TokenAPIView.as_view(), name="token"),

	path('api/admin/register/', AdminRegistrationAPIView.as_view(), name="register_admin"),

    path('api/manufacturer-user/register/', ManufacturerUserRegistrationAPIView.as_view(), name="register_manufactureruser"),

    path('api/manufacturer/{id}/manufacturer-users', ManufacturerViewSet),


]
