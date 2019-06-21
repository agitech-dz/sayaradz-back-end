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
from rest_framework import routers
from sayaradz import views 
from rest_framework.authtoken import views as rest_framework_views
from rest_framework.documentation import include_docs_urls 
import notifications.urls

# Routers provide an easy way of automatically determining the URL conf.

router = routers.DefaultRouter()

router.register(r'api/admins', views.UserViewSet)

router.register(r'api/manufacturers', views.ManufacturerViewSet, base_name='manufacturers')

router.register(r'api/manufacturers-users', views.ManufacturerUserViewSet)

router.register(r'api/models', views.MyModelViewSet)

router.register(r'api/options', views.OptionViewSet)

router.register(r'api/versions', views.VersionViewSet)

router.register(r'api/colors', views.ColorViewSet)

router.register(r'api/tarifs-versions', views.LigneTarifVersionViewSet)

router.register(r'api/tarifs-options', views.LigneTarifOptionViewSet)

router.register(r'api/tarifs-colors', views.LigneTarifColorViewSet)

router.register(r'api/newcars', views.NewCarViewSet)

router.register(r'api/automobilists', views.AutomobilistViewSet)

router.register(r'api/automobilist/ads', views.AdViewSet)

#router.register(r'api/automobilist/follow-model-or-version', views.AutomobilistViewSet1)

#router.register(r'api/automobilist/unfollow-model-or-version', views.AutomobilistViewSet2)

router.register(r'api/commands', views.CommandViewSet)

router.register(r'api/automobilist/followed-models', views.FollowedModelsViewSet)

router.register(r'api/automobilist/followed-versions', views.FollowedVersionsViewSet)

# Wire up our API using automatic URL routing.

# Additionally, we include login URLs for the browsable API.

urlpatterns = [

    path('admin/', admin.site.urls),    

    path(r'', include(router.urls)),

    path(r'api/', include('rest_framework.urls', namespace='rest_framework')),

    path(r'api/docs', include_docs_urls(title='Sayara DZ API')),

    path(r'api/manufacturers-user-filter', views.ManufacturerUserList.as_view(), name="manufactureruser_filter"),

    path(r'api/manufacturers-filter', views.ManufacturerList.as_view(), name="manufacturer_filter"),

    path('api/admin/login/', views.AdminLoginAPIView.as_view(), name="login_admin"),

    path('api/manufacturer-user/login', views.ManufacturerUserLoginAPIView.as_view(), name="login_manufactureruser"),

    path('api/admin/logout', views.LogoutView.as_view(), name="logout_admin"),

    path('api/manufacturer-user/logout', views.LogoutView.as_view(), name="logout_manufactureruser"),

    #path('tokens/<key>/', TokenAPIView.as_view(), name="token"),

	path('api/admin/register/', views.AdminRegistrationAPIView.as_view(), name="register_admin"),

    path('api/manufacturer-user/register/', views.ManufacturerUserRegistrationAPIView.as_view(), name="register_manufactureruser"),

    path('api/models-filter', views.MyModelList.as_view(), name="model_filter"),

    path('api/automobilist/manufacturers', views.AutomobilistManufacturerViewSet.as_view(), name='automobilist_manufacturers'),

    path('api/automobilist/<manufacturer>/models', views.AutomobilistMyModelViewSet.as_view(), name='automobilist_models'),

    path('api/automobilist/<model>/versions', views.AutomobilistVersionViewSet.as_view(), name='automobilist_versions'),

    path('api/automobilist/option-price/<code>', views.ComposeCarView.as_view(), name='option_price'),

    path('api/automobilist/version-price/<code>', views.ComposeCarView.as_view(), name='version_price'),

    path('api/automobilist/newcars-filter', views.NewCarList.as_view(), name='newcar_filter'),

    path('api/automobilist/association-exists/<manufacturer>/<model>/<version>', views.ManufacturerModelVersioAssociationView.as_view(), name='associations_exists'),

    path('api/automobilist/ads-filter', views.AdList.as_view(), name='ad_filter'),

    path('api/automobilist/post-offer', views.OfferPostView.as_view(), name='post_offer'),

    path('api/automobilist/get-ad-offers/<ad>', views.AdOfferGetView.as_view(), name='get_ad_offer'),
    
    path('api/automobilist/get-automobilist-offers/<automobilist>', views.AutomobilistOfferGetView.as_view(), name='get_automobilist_offer'),

    path('api/automobilist/accept-offer/<int:pk>', views.OfferUpdateView.as_view(), name='update_offer'),

    path('api/automobilist/<model>/colors', views.AutomobilistModelColorViewSet.as_view(), name='automobilist_models_colors'),

    path('api/automobilist/colors', views.AutomobilistColorViewSet.as_view(), name='automobilist_colors'),

    path('api/inbox/notifications/', include(notifications.urls, namespace='notifications')),

    path('api/automobilist/offers-notifications/<recipient>', views.AutomobilistOfferAcceptNotificationView.as_view(), name='accept_offers_notifications'),

    path('api/automobilist/commands-notifications/<recipient>', views.AutomobilistCommandValidatedNotificationView.as_view(), name='validate_commands_notifications'),

    path('api/commands/validate-command/<int:manufacturer_user>/<int:command_pk>', views.CommandUpdateView.as_view(), name='validate_command'),

    path('api/automobilist/post-command', views.CommandPostView.as_view(), name='post_command'),

    path('api/automobilist/automobilist-followed-models', views.FollowedModelsList.as_view(), name='get_followed_models'),

    path('api/automobilist/automobilist-followed-versions', views.FollowedVersionsList.as_view(), name='get_followed_versions'),

]
