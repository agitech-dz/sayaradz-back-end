from django.urls import path, include
from django.contrib import admin

from . import views
from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'languages', views.LanguageView)


urlpatterns = [
    path('', views.index),
    path(r'a/', include(router.urls)),

    #path(r'api/', include('rest_framework.urls', namespace='rest_framework'))
]
