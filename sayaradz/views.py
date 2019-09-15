import django_filters
from rest_framework import filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import logout
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from sayaradz_api import serializers 
from sayaradz import models
from rest_framework import status
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveDestroyAPIView, GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from notifications.signals import notify
from django.http import Http404
from rest_framework import generics
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import facebook
from rest_framework.authtoken.models import Token
import json
#from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from google.auth.transport import requests
from google.oauth2 import id_token




"""
UserViewSet
"""
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()

    serializer_class = serializers.AdminSerializer

"""
Define the pagination logic
"""
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 25


"""
ManufacturerViewSet : get, delete, patch, partial_update, put, paginated output
"""
class ManufacturerViewSet(viewsets.ModelViewSet):
	pagination_class = StandardResultsSetPagination
	permission_classes = (IsAuthenticated,)  

	queryset = models.Manufacturer.objects.all()
	serializer_class = serializers.ManufacturerSerializer
	#filter_backends = (DjangoFilterBackend,)
	#filter_fields = ('name', 'nationality')
	def list(self, request,*kwargs):
		queryset = models.Manufacturer.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		count = models.Manufacturer.objects.all().count()
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response({
			'results':data,
			'meta':{
				'count':count
				},
			})

	def destroy(self, *args, **kwargs):
         serializer = self.get_serializer(self.get_object())
         super().destroy(*args, **kwargs)
         return Response(serializer.data, status=status.HTTP_200_OK)




"""
ManufacturerUserViewSet : get, delete, patch, partial_update, put, paginated output
"""
class ManufacturerUserViewSet(viewsets.ModelViewSet):
	pagination_class = StandardResultsSetPagination
	permission_classes = (IsAuthenticated, IsAdminUser)  
	queryset = models.ManufacturerUser.objects.all()
	serializer_class = serializers.ManufacturerUserSerializer
	parser_classes = (MultiPartParser, FormParser)
	def list(self, request,*kwargs):
		queryset = models.ManufacturerUser.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		count1 = models.ManufacturerUser.objects.all().count()
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data

		return Response({
			'results':data,
			'meta':{
				'count':count1
				},
			})

"""
AdminRegistrationAPIView : post only, allows to create new admin account
"""
class AdminRegistrationAPIView(CreateAPIView):
	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.AdminRegistrationSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		user = serializer.instance
		user.is_superuser = True
		user.is_staff = True
		user.save()
		token, created = Token.objects.get_or_create(user=user)
		data = serializer.data
		data["token"] = token.key

		headers = self.get_success_headers(serializer.data)
		return Response(data, status=status.HTTP_201_CREATED, headers=headers)

"""
ManufacturerUserRegistrationAPIView : post only, allows to create new manufacturer user account
"""
class ManufacturerUserRegistrationAPIView(CreateAPIView):
	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.ManufacturerUserRegistrationSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)

		user = serializer.instance
		token, created = Token.objects.get_or_create(user=user)
		data = serializer.data
		data["token"] = token.key

		headers = self.get_success_headers(serializer.data)
		return Response(data, status=status.HTTP_201_CREATED, headers=headers)

class TokenAPIView(RetrieveDestroyAPIView):

	lookup_field = "key"
	serializer_class = serializers.TokenSerializer
	queryset = Token.objects.all()

	def filter_queryset(self, queryset):
		return queryset.filter(user=self.request.user)

	def retrieve(self, request, key, *args, **kwargs):

		if key == "current":
			instance = Token.objects.get(key=request.auth.key)
			serializer = self.get_serializer(instance)
			return Response(serializer.data)
		return super(TokenAPIView, self).retrieve(request, key, *args, **kwargs)

	def destroy(self, request, key, *args, **kwargs):
		if key == "current":
			Token.objects.get(key=request.auth.key).delete()
			return Response(status=status.HTTP_204_NO_CONTENT)

		return super(TokenAPIView, self).destroy(request, key, *args, **kwargs)


"""
ManufacturerUserLoginAPIView : post only, allows manufacturer user authentification
"""
class UserLoginAPIView(GenericAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.UserLoginSerializer
	
	def post(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			
			user = serializer.user
			
			token, _ = Token.objects.get_or_create(user=user)

			return Response(
				data=serializers.TokenSerializer(token).data,
				status=status.HTTP_200_OK,
			)

		else:
			
			return Response(
				data=serializer.errors,
				status=status.HTTP_400_BAD_REQUEST,
			)
"""
LogoutView : post only, allows users logout
"""
class LogoutView(GenericAPIView):

	serializer_class = serializers.UserLoginSerializer
	def post(self, request):

		django_logout(request)
		return Response(status=204)

"""
ManufacturerUserFilter : filter ManufacturerUser output data by ['address', 'first_name','manufacturer', 'manufacturer__name']
"""
class ManufacturerUserFilter(django_filters.FilterSet):
	class Meta:
		model = models.ManufacturerUser
		fields = ['address', 'first_name','manufacturer', 'manufacturer__name']

"""
ManufacturerUserList : Get only, allows to get ManufacturerUser output data 
 : using  	filtering by ['address', 'first_name','manufacturer', 'manufacturer__name'],
			Search
			ordering
"""
class ManufacturerUserList(ListAPIView):

	permission_classes = (IsAuthenticated,)  
	queryset = models.ManufacturerUser.objects.all()
	serializer_class = serializers.ManufacturerUserSerializer
	filter_class = ManufacturerUserFilter
	filter_backends = (filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend,)
	search_fields = ('username', 'email', 'address', 'manufacturer__name')
	ordering_fields = '__all__'
	

"""
ManufacturerUserFilter : filter ManufacturerUser output data by ['id', 'name', 'nationality']
"""
class ManufacturerFilter(django_filters.FilterSet):
	class Meta:
		model = models.Manufacturer
		fields = ['id', 'name', 'nationality']

"""
ManufacturerList : Get only, allows to get Manufacturer output data 
 : using  	filtering by ['address', 'first_name','manufacturer', 'manufacturer__name'],
			Search
			ordering
"""
class ManufacturerList(ListAPIView):
	
	permission_classes = (IsAuthenticated,)  
	queryset = models.Manufacturer.objects.all()

	serializer_class = serializers.ManufacturerSerializer
	filter_class = ManufacturerFilter
	filter_backends = (filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend,)
	search_fields = ('name', 'nationality')	
	ordering_fields = '__all__'

	
"""
ModelViewSet : get, delete, patch, partial_update, put, paginated output
"""
class MyModelViewSet(viewsets.ModelViewSet):

	pagination_class = StandardResultsSetPagination
	permission_classes = (IsAuthenticated,)  
	queryset = models.MyModel.objects.all()
	serializer_class = serializers.MyModelSerializer

	def list(self, request,*kwargs):
		queryset = models.MyModel.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response({'results':data})

	def partial_update(self, request,*kwargs, pk):

		queryset = models.MyModel.objects.get(pk= pk)

		serializer = serializers.MyModelSerializer(queryset, data=request.data, partial=True)
		# get current manufacturer user
		user = serializers.ManufacturerUserSerializer(request.user).instance
		
		if serializer.is_valid():

			serializer.save()
			#add notification post offer
			"""
			actor: manufacturer changed 
			action_objet: model
			recepient: automobilist
			verb: model name
			target: model 
			model : followed model
			"""
			model_ = serializer.instance
			image = model_.image
			actor = user
			verb = model_.name
			target = model_
			target_object_id = model_.code
			action_object=model_
			followers = models.FollowedModels.objects.filter(model=model_.code)
			for follower in followers:

				recipient =  follower.automobilist #smodels.Automobilist.objects.get(pk=follower.automobilist) #receive notification
				notification = models.AutomobilistFollowedModelChangeNotification(actor= actor, recipient= recipient, verb= verb, target_object_id= target_object_id, target= target, model= model_, notification_type= "MC", image=image, action_object=action_object)
				notification.save()
			#serializer = serializers.AutomobilistAcceptOfferNotificationSerializer(notification)
			return Response(serializer.data)
		# return a meaningful error response
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
MyModelFilter : filter Model output data by ['code', 'name','manufacturer', 'manufacturer__name']
"""
class MyModelFilter(django_filters.FilterSet):
	class Meta:
		model = models.MyModel
		fields = ['code', 'name', 'manufacturer', 'manufacturer__name']

"""
MyModelList : Get only, allows to get ManufacturerUser output data 
 : using  	filtering by ['code', 'name', 'manufacturer__name'],
			Search
			ordering
"""
class MyModelList(ListAPIView):

	permission_classes = (IsAuthenticated,)  
	queryset = models.MyModel.objects.all()
	serializer_class = serializers.MyModelSerializer
	filter_class = MyModelFilter
	filter_backends = (filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend,)
	search_fields = ( 'code', 'name', 'manufacturer__name')
	ordering_fields = '__all__'

"""
OptionViewSet : get, delete, patch, partial_update, put, paginated output
"""
class OptionViewSet(viewsets.ModelViewSet):

	#pagination_class = StandardResultsSetPagination
	permission_classes = (IsAuthenticated,)  
	queryset = models.Option.objects.all()
	serializer_class = serializers.OptionSerializer
	pagination_class = StandardResultsSetPagination
	def list(self, request,*kwargs):
		queryset = models.Option.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response({'results':data})

"""
VersionViewSet : get, delete, patch, partial_update, put, paginated output
"""
class VersionViewSet(viewsets.ModelViewSet):

	pagination_class = StandardResultsSetPagination
	permission_classes = (IsAuthenticated,)  
	queryset = models.Version.objects.all().prefetch_related('options')
	serializer_class = serializers.VersionSerializer

	def list(self, request,*kwargs):
		queryset = models.Version.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response({'results':data})

	def partial_update(self, request,*kwargs, pk):

		queryset = models.Version.objects.get(pk= pk)

		serializer = serializers.VersionSerializer(queryset, data=request.data, partial=True)
		# get current manufacturer user
		user = serializers.ManufacturerUserSerializer(request.user).instance
		
		if serializer.is_valid():

			serializer.save()
			#add notification post offer
			"""
			actor: manufacturer changed 
			action_objet: version
			recepient: automobilist
			verb: model name
			target: model 
			model : followed model
			"""
			version_ = serializer.instance
			image = version_.image
			actor = user
			verb = version_.name
			target = version_
			target_object_id = version_.code
			action_object=version_
			followers = models.FollowedVersions.objects.filter(version=version_.code)
			for follower in followers:

				recipient =  follower.automobilist #smodels.Automobilist.objects.get(pk=follower.automobilist) #receive notification
				notification = models.AutomobilistFollowedVersionChangeNotification(actor= actor, recipient= recipient, verb= verb, target_object_id= target_object_id, target= target, version= version_, notification_type= "VC", image=image, action_object=action_objet)
				notification.save()
			#serializer = serializers.AutomobilistAcceptOfferNotificationSerializer(notification)
			return Response(serializer.data)
		# return a meaningful error response
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
ColorViewSet : get, delete, patch, partial_update, put, paginated output
"""
class ColorViewSet(viewsets.ModelViewSet):

	pagination_class = StandardResultsSetPagination
	permission_classes = (IsAuthenticated,)  

	queryset = models.Color.objects.all()
	serializer_class = serializers.ColorSerializer

	def list(self, request,*kwargs):
		queryset = models.Color.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response({'results':data})


"""
AutomobilistManufacturerViewSet : get (read only endpoint)
"""
class AutomobilistManufacturerViewSet(ListAPIView):
	queryset = models.Manufacturer.objects.all()
	serializer_class = serializers.ManufacturerSerializer
	

"""
AutomobilistMyModelViewSet : get (read only endpoint) paginated output
"""
class AutomobilistMyModelViewSet(ListAPIView):
	
	queryset = models.MyModel.objects.all()
	serializer_class = serializers.MyModelSerializer

	def list(self, request,*kwargs, manufacturer):
		queryset = models.MyModel.objects.filter(manufacturer= manufacturer)
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response(data)

"""
AutomobilistVersionViewSet : get (Read only endpoint) paginated output
"""
class AutomobilistVersionViewSet(ListAPIView):

	queryset = models.Version.objects.all().prefetch_related('options')
	serializer_class = serializers.VersionSerializer

	def list(self, request,*kwargs, model):
		if model == "all":
			queryset = models.Version.objects.all()
		else:
			queryset = models.Version.objects.filter(model= model)

		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response(data)

"""
AutomobilistModelColorViewSet : get colors related to a model
"""
class AutomobilistModelColorViewSet(ListAPIView):

	queryset = models.Color.objects.all()
	serializer_class = serializers.ColorSerializer

	def list(self, request,*kwargs, model):

		queryset = models.Color.objects.filter(model_id= model)
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response(data)

"""
AutomobilistColorViewSet : get all colors
"""
class AutomobilistColorViewSet(ListAPIView):

	queryset = models.Color.objects.all()
	serializer_class = serializers.ColorSerializer

"""
AutomobilistModelOptionViewSet : get options related to a model
"""
class AutomobilistModelOptionViewSet(ListAPIView):

	queryset = models.Option.objects.all()
	serializer_class = serializers.OptionSerializer

	def list(self, request,*kwargs, model):

		queryset = models.Option.objects.filter(model_id= model)
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response(data)

"""
AutomobilistOptionViewSet : get all options
"""
class AutomobilistOptionViewSet(ListAPIView):

	queryset = models.Option.objects.all()
	serializer_class = serializers.OptionSerializer

"""
AutomobilistViewSet1
"""
class AutomobilistViewSet1(mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

	queryset = models.Automobilist.objects.all().prefetch_related('followedModels').prefetch_related('followedVersions')
	http_method_names = ('put', 'patch', 'get')
	serializer_class = serializers.AutomobilistSerializer1
	

"""
AutomobilistViewSet2 #delete 
"""
class AutomobilistViewSet2(mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = models.Automobilist.objects.all().prefetch_related('followedModels').prefetch_related('followedVersions')
    http_method_names = ('put', 'patch')
    serializer_class = serializers.AutomobilistSerializer2

"""
LigneTarifVersionViewSet
"""
class LigneTarifVersionViewSet(viewsets.ModelViewSet):

	queryset = models.LigneTarifVersion.objects.all()

	serializer_class = serializers.LigneTarifVersionSerializer
	
	pagination_class = StandardResultsSetPagination
	def list(self, request,*kwargs):
		queryset = models.LigneTarifVersion.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response({'results':data})

"""
LigneTarifOptionViewSet
"""
class LigneTarifOptionViewSet(viewsets.ModelViewSet):

	queryset = models.LigneTarifOption.objects.all()

	serializer_class = serializers.LigneTarifOptionSerializer
	
	pagination_class = StandardResultsSetPagination
	def list(self, request,*kwargs):
		queryset = models.LigneTarifOption.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response({'results':data})

"""
LigneTarifColorViewSet
"""
class LigneTarifColorViewSet(viewsets.ModelViewSet):
	queryset = models.LigneTarifColor.objects.all()
	serializer_class = serializers.LigneTarifColorSerializer
	pagination_class = StandardResultsSetPagination
	def list(self, request,*kwargs):
		queryset = models.LigneTarifColor.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response({'results':data})
	

"""
NewCarViewSet
"""
class NewCarViewSet(viewsets.ModelViewSet):

	queryset = models.NewCar.objects.all()
	serializer_class = serializers.NewCarSerializer
	pagination_class = StandardResultsSetPagination
	parser_classes = (MultiPartParser, FormParser)
	def list(self, request,*kwargs):
		queryset = models.NewCar.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response({'results':data})


"""
AutomobilistViewSet
"""
class AutomobilistViewSet(viewsets.ModelViewSet):

    queryset = models.Automobilist.objects.all()
    serializer_class = serializers.AutomobilistSerializer

"""
Composer Véhicule
"""
class ComposeCarView(APIView):

	def get_object(self, code):
		versionPrice = False
		optionPrice = False

		try:
			price =  models.LigneTarifVersion.objects.get(code=code).price
			versionPrice = True

		except models.LigneTarifVersion.DoesNotExist:
			try:
				price =  models.LigneTarifOption.objects.get(code=code).price
				optionPrice = True

			except models.LigneTarifOption.DoesNotExist:
				raise Http404

		return price

	def get(self, request, code, format=None):
		print(code)
		price = self.get_object(code)
		data={
			'price': price
		}
		return Response(data)


"""
NewCarFilter : filter New Cars output data by ['code', 'name','manufacturer', 'manufacturer__name']
"""
class NewCarFilter(django_filters.FilterSet):
	options= django_filters.ModelMultipleChoiceFilter(queryset=models.Option.objects.all())

	class Meta:
		model = models.NewCar
		fields = ['numChassis', 'color','version', 'options', 'color__name', 'isExisted']

"""
NewCarList : Get only, allows to get New Car output data 
 : using  	filtering by ['numChassis', 'color','version', 'options'],
			Search
			ordering
"""
class NewCarList(ListAPIView):

	permission_classes = (IsAuthenticated,)  
	queryset = models.NewCar.objects.all()
	serializer_class = serializers.NewCarSerializer
	filter_class = NewCarFilter
	filter_backends = (filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend,)
	search_fields = ('numChassis', 'color','version', 'options')
	ordering_fields = '__all__'

"""
Composer Véhicule
"""
class ManufacturerModelVersioAssociationView(APIView):

	def get_object(self, manufacturer, model, version):
		
		if(models.MyModel.objects.filter(manufacturer=manufacturer, code=model).exists()):

			if(models.Version.objects.filter(model=model, code=version).exists()):
				return True	

			else: 
				return False

		else:
			return False

	def get(self, request, manufacturer, model, version, format=None):

		exists = self.get_object(manufacturer, model, version)
		data={
			'exists': exists
		}
		return Response(data)

"""
AdFilter : filter Ads (Annonces) output data by ['id','model', 'model__name', 'version', 'version__name', 'manufacturer', 'manufacturer__name', 'minPrice', 'date', 'automobilist', 'automobilist__firstName', 'automobilist__familyName']
"""
class AdFilter(django_filters.FilterSet):
	class Meta:
		model = models.Ad
		fields = ['id','model', 'model__name', 'version', 'version__name', 'manufacturer', 'manufacturer__name', 'minPrice', 'date', 'automobilist', 'automobilist__first_name', 'automobilist__last_name', 'automobilist__username']

"""
AdList : Get only, allows to get Ad output data 
 : using  	filtering by ['id','model', 'model__name', 'version', 'version__name', 'manufacturer', 'manufacturer__name', 'minPrice', 'date', 'automobilist', 'automobilist__firstName', 'automobilist__familyName'],
			Search
			ordering
"""
class 	AdList(ListAPIView):

	#permission_classes = (IsAuthenticated,)  
	queryset = models.Ad.objects.all()
	serializer_class = serializers.AdSerializer
	filter_class = AdFilter
	filter_backends = (filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend,)
	search_fields = ('model__name', 'version__name', 'manufacturer__name', 'minPrice', 'date', 'automobilist__first_name', 'automobilist__last_name', 'automobilist__username', 'year', 'distance' )
	ordering_fields = '__all__'

"""
AutomobilistMyModelViewSet : get (read only endpoint) paginated output
"""
class AdViewSet(viewsets.ModelViewSet):

	#pagination_class = StandardResultsSetPagination
	#permission_classes = (IsAuthenticated,)  
	queryset = models.Ad.objects.all()
	serializer_class = serializers.AdSerializer
	parser_classes = (MultiPartParser, FormParser)
	def list(self, request,*kwargs):
		queryset = models.Ad.objects.all()
		#page = self.paginate_queryset(queryset)
		#if page is not None:
		#	serializer = self.get_serializer(page, many=True)
		#	return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response(data)

"""
OfferPostView : Poster une annonce
"""
class OfferPostView(CreateAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.OfferSerializer

	def create(self, request, *args, **kwargs):
		
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():

			serializer.save()
			#add notification post offer
			"""
			actor : sender(Automobilist_id offer owner)
			recipient: ad owner
			description: phone number
			verb: offered price
			target_object_id = ad id (target ad)
			offer: offer id
			adOwner:
			"""
			offer = serializer.instance
			image = offer.ad.photo1
			ad_ = models.Ad.objects.get(pk= offer.ad_id)
			recipient =  ad_.automobilist#receive notification
			actor = models.Automobilist.objects.get(pk= offer.automobilist_id)
			verb = offer.offredPrice
			target_object_id = ad_.id
			target = ad_
			action_object=offer

			notification = models.AutomobilistPostOfferNotification(actor= actor, recipient= recipient, verb= verb, target_object_id= target_object_id, target= target, offer= offer, notification_type= "PO", image=image, action_objet=action_objet)
			notification.save()
			#serializer = serializers.AutomobilistAcceptOfferNotificationSerializer(notification)
			return Response(serializer.data)
		# return a meaningful error response
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




"""
AdOfferGetView : Get ad offers
"""
class AdOfferGetView(APIView):

	serializer_class = serializers.OfferSerializer

	def get_queryset(self, ad):

		try:
			
			return models.Offer.objects.filter(ad=ad)

		except models.Offer.DoesNotExist:

			raise Http404

	def get_object(self, ad):
		
		try:
			
			serializer = serializers.OfferSerializer(self.get_queryset(ad), many=True)
			return Response(serializer.data)

		except models.Offer.DoesNotExist:

			raise Http404

	def get(self, request, ad, format=None):

		return self.get_object(ad)

"""
AutomobilistOfferGetView : Get automobilist offers
"""
class AutomobilistOfferGetView(APIView):
	
	serializer_class = serializers.OfferSerializer

	def get_queryset(self, automobilist):

		try:
			
			return models.Offer.objects.filter(automobilist=automobilist)

		except models.Offer.DoesNotExist:

			raise Http404

	def get_object(self, automobilist):
		
		try:
			
			serializer = serializers.OfferSerializer(self.get_queryset(automobilist), many=True)
			return Response(serializer.data)

		except models.Offer.DoesNotExist:

			raise Http404

	def get(self, request, automobilist, format=None):
	 
		return self.get_object(automobilist)



"""
OfferUpdateView : Poster une annonce
"""
class OfferUpdateView(UpdateAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.OfferSerializer

	def get_queryset(self, pk):

		try:
			return models.Offer.objects.get(pk=pk)

		except models.Offer.DoesNotExist:

			raise Http404

	def patch(self, request, pk):
		try:
			# if no model exists by this PK, raise a 404 error
			offer = self.get_queryset(pk)

		except models.Offer.DoesNotExist:

			raise Http404
		
		#ad = offer.ad
		# this is the only field we want to update
		data = {"isAccepted": True}

		serializer = serializers.OfferSerializer(offer, data=data, partial=True)

		if serializer.is_valid():

			serializer.save()
			#add notification
			"""
			actor : ad owner
			recipient: accepted offer owner
			description: phone number
			verb: offered price
			target_object_id = ad id (target ad)
			offer: offer id
			adOwner:
			

			"""
			ad_ = models.Ad.objects.get(pk= offer.ad_id)
			image = ad_.photo1
			recipient =  offer.automobilist#receive notification
			actor = models.Automobilist.objects.get(pk= ad_.automobilist_id)
			adOwner = actor.id
			verb = offer.offredPrice
			target_object_id = ad_.id
			target = ad_
			action_object= offer

			notification = models.AutomobilistAcceptOfferNotification(actor= actor, recipient= recipient, verb= verb, target_object_id= target_object_id, target= target, offer= offer, notification_type="OA", image=image, action_object=action_object)
			notification.save()
			#serializer = serializers.AutomobilistAcceptOfferNotificationSerializer(notification)
			return Response(serializer.data)
		# return a meaningful error response
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
AutomobilistOfferAcceptNotificationView : A
"""
class AutomobilistOfferAcceptNotificationView(ListAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.AutomobilistAcceptOfferNotificationSerializer

	def get_queryset(self, recipient):

		try:
			return models.AutomobilistAcceptOfferNotification.objects.filter(recipient = recipient)

		except models.AutomobilistAcceptOfferNotification.DoesNotExist:

			raise Http404


	def list(self, request,*kwargs, recipient):
		queryset = self.get_queryset(recipient)
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response(data)

"""
AutomobilistOfferPostNotificationView : A
"""
class AutomobilistOfferPostNotificationView(ListAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.AutomobilistPostOfferNotificationSerializer

	def get_queryset(self, recipient):

		try:
			return models.AutomobilistPostOfferNotification.objects.filter(recipient = recipient)

		except models.AutomobilistPostOfferNotification.DoesNotExist:

			raise Http404

	def list(self, request,*kwargs, recipient):
		queryset = self.get_queryset(recipient)
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response(data)


"""
CommandViewSet : list commands and delete command
"""
class CommandViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):

	queryset = models.Command.objects.all()
	http_method_names = ('get', 'delete', 'patch')
	serializer_class = serializers.CommandSerializer
	pagination_class = StandardResultsSetPagination
	def list(self, request,*kwargs):
		queryset = models.Command.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response({'results':data})



"""
AutomobilistFollowedModelChangedNotificationView : A
"""
class AutomobilistFollowedModelChangedNotificationView(ListAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.AutomobilistFollowedModelChangedNotificationSerializer

	def get_queryset(self, recipient):

		try:
			return models.AutomobilistFollowedModelChangedNotification.objects.filter(recipient = recipient)

		except models.AutomobilistFollowedModelChangedNotification.DoesNotExist:

			raise Http404

	def list(self, request,*kwargs, recipient):
		queryset = self.get_queryset(recipient)
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response(data)


"""
AutomobilistCommandValidatedNotificationNotificationView : A
"""
class AutomobilistCommandValidatedNotificationView(ListAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.AutomobilistCommandValidatedNotificationSerializer

	def get_queryset(self, recipient):

		try:
			return models.AutomobilistCommandValidatedNotification.objects.filter(recipient = recipient)

		except models.AutomobilistCommandValidatedNotification.DoesNotExist:

			raise Http404

	def list(self, request,*kwargs, recipient):
		queryset = self.get_queryset(recipient)
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response(data)

"""
AutomobilistFollowedModelChangedNotificationView : A
"""
class AutomobilistFollowedModelChangedNotificationView(ListAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.AutomobilistFollowedModelChangedNotificationSerializer

	def get_queryset(self, recipient):

		try:
			return models.AutomobilistFollowedModelChangeNotification.objects.filter(recipient = recipient)

		except models.AutomobilistFollowedModelChangeNotification.DoesNotExist:

			raise Http404

	def list(self, request,*kwargs, recipient):
		queryset = self.get_queryset(recipient)
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response(data)

"""
AutomobilistFollowedModelChangedNotificationView : A
"""
class AutomobilistFollowedVersionChangedNotificationView(ListAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.AutomobilistFollowedVersionChangedNotificationSerializer

	def get_queryset(self, recipient):

		try:
			return models.AutomobilistFollowedVersionChangeNotification.objects.filter(recipient = recipient)

		except models.AutomobilistFollowedVersionChangeNotification.DoesNotExist:

			raise Http404

	def list(self, request,*kwargs, recipient):
		queryset = self.get_queryset(recipient)
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response(data)


"""
CommandUpdateView : Validate command
"""
class CommandUpdateView(UpdateAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.CommandSerializer

	def patch(self, request, command_pk, manufacturer_user):
		#serializer_class = serializers.MinCommandSerializer		
		try:
			# if no model exists by this PK, raise a 404 error
			command = models.Command.objects.get(pk=command_pk)
			manufacturerUser = models.ManufacturerUser.objects.get(pk=manufacturer_user)

		except models.Command.DoesNotExist:

			raise Http404
		
		#ad = offer.ad
		# this is the only field we want to update
		data = {"isValidated": True}

		serializer = serializers.CommandSerializer(command, data=data, partial=True)

		if serializer.is_valid():

			serializer.save()
			car_data = {"isExisted": False}
			#delete car from stock
			car = models.NewCar.objects.get(pk=command.car)

			car_serializer = serializers.NewCarSerializer(car, data=car_data, partial=True)
			if car_serializer.is_valid():
				car_serializer.save()
				#add notification
				"""
				actor : manufacturer user
				recipient: command owner
				verb: Manufacturer Name (Marque)
				target = command
				"""
				recipient =  command.automobilist#receive notification
				actor = manufacturerUser
				verb = models.Manufacturer.objects.get(pk= manufacturerUser.manufacturer_id).name
				target = command
				image=target.car.photo1
				action_objet=car
				
				notification = models.AutomobilistCommandValidatedNotification(actor= actor, recipient= recipient, verb= verb, target= target, notification_type='CV', image=image, action_objet=action_object)
				notification.save()
				#serializer = serializers.AutomobilistAcceptOfferNotificationSerializer(notification)
				return Response(serializer.data)
		# return a meaningful error response
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
CommandPostView : post only, allows to create new command
"""
class CommandPostView(CreateAPIView):
	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.CommandSerializer
	

"""
FollowedModelsViewSet : get (read only endpoint) paginated output
"""
class FollowedVersionsViewSet(viewsets.ModelViewSet):

	#permission_classes = (IsAuthenticated,)  
	queryset = models.FollowedVersions.objects.all()
	serializer_class = serializers.FollowedVersionsSerializer

"""
FollowedModelsViewSet : get (read only endpoint) paginated output
"""
class FollowedModelsViewSet(viewsets.ModelViewSet):

	#permission_classes = (IsAuthenticated,)  
	queryset = models.FollowedModels.objects.all()
	serializer_class = serializers.FollowedModelsSerializer


"""
ManufacturerUserFilter : filter ManufacturerUser output data by ['address', 'first_name','manufacturer', 'manufacturer__name']
"""
class FollowedModelsFilter(django_filters.FilterSet):
	class Meta:
		model = models.FollowedModels
		fields = ['model', 'automobilist', 'date', "model__name"]

"""
FollowedModelsList : Get only, allows to 
"""
class FollowedModelsList(ListAPIView):

	queryset = models.FollowedModels.objects.all()
	serializer_class = serializers.FollowedModelsSerializer
	filter_class = FollowedModelsFilter
	filter_backends = (filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend,)
	search_fields = ('model', 'automobilist', 'date', 'automobilst__username', "model__name")
	ordering_fields = '__all__'



"""
ManufacturerUserFilter : filter ManufacturerUser output data by ['address', 'first_name','manufacturer', 'manufacturer__name']
"""
class FollowedVersionsFilter(django_filters.FilterSet):
	class Meta:
		model = models.FollowedVersions
		fields = ['version', 'automobilist', 'date', "version__name"]

"""
FollowedModelsList : Get only, allows to 
"""
class FollowedVersionsList(ListAPIView):

	queryset = models.FollowedVersions.objects.all()
	serializer_class = serializers.FollowedVersionsSerializer
	filter_class = FollowedVersionsFilter
	filter_backends = (filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend,)
	search_fields = ('version', 'automobilist', 'date', 'automobilst__username', "model__name")
	ordering_fields = '__all__'


"""
FollowedModelsList : Get only, allows to 
"""
class NewCarsStockView(generics.ListCreateAPIView):

	permission_classes = (IsAuthenticated,) 
	model = models.NewCar
	serializer_class = serializers.NewCarSerializer
	queryset = models.NewCar.objects.all()

	def create(self, request, *args, **kwargs):
		print(request.data)
		for element in request.data :
			
			options_list = element["options"].split(";")
			element["options"] = options_list
		
		serializer = self.get_serializer(data=request.data, many=True)
		if serializer.is_valid():
			serializer.save()
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TarifsUploadView(generics.CreateAPIView):

	permission_classes = (IsAuthenticated,) 
	model = models.LigneTarif
	type = "0"
	
	def create(self, request, *args, **kwargs):
		ligneTarifVersion = []
		ligneTarifColor = []
		ligneTarifOption = []

		allData = []

		for element in request.data :
			 
			if element["type"] == "0":
				del element["type"]
				ligneTarifVersion.append(element)

			elif element["type"] == "1":
				del element["type"]
				ligneTarifColor.append(element)

			elif element["type"] == "2":
				del element["type"]
				ligneTarifOption.append(element)
		
		print(ligneTarifVersion)

		serializer = self.get_serializer(data=ligneTarifVersion, many=True)
		if serializer.is_valid():
			serializer.save()
			headers = self.get_success_headers(serializer.data)
			allData.extend(serializer.data)

		else:

			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		self.type = "1"
		serializer = self.get_serializer(data=ligneTarifColor, many=True)
		if serializer.is_valid():
			serializer.save()
			headers = self.get_success_headers(serializer.data)
			allData.extend(serializer.data)

		else:

			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		self.type = "2"
		serializer = self.get_serializer(data=ligneTarifOption, many=True)
		if serializer.is_valid():
			serializer.save()
			headers = self.get_success_headers(serializer.data)
			allData.extend(serializer.data)

		else:

			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			
		return Response(allData, status=status.HTTP_201_CREATED, headers=headers)
		
		

	def get_serializer_class(self):

		if self.type == "0":
			return serializers.LigneTarifVersionSerializer

		elif self.type == "1":
			return serializers.LigneTarifColorSerializer

		return serializers.LigneTarifOptionSerializer

	def get_queryset(self):

		if self.type == "0":
			return models.LigneTarifVersion.objects.all()

		if self.type == "1":
			return models.LigneTarifColor.objects.all()

		return models.LigneTarifOption.objects.all()

"""
TransactionViewSet
"""
class TransactionViewSet(viewsets.ModelViewSet):

    queryset = models.Transaction.objects.all()

    serializer_class = serializers.TransactionSerializer


"""
Composer vehiule dispo 
"""
class NewCarsFilterView(generics.ListCreateAPIView):

	model = models.NewCar
	serializer_class = serializers.NewCarSerializer
	queryset = models.NewCar.objects.all()

	def create(self, request, *args, **kwargs):
		print(request.data)

			
		version = request.data["version"]
		cars = models.NewCar.objects.filter(version=version, isExisted=True)
		if request.data["color"] is not None:
			color = request.data["color"]
			cars = models.NewCar.objects.filter(color=color)
			
		options=request.data["options"]
		
		for option in options:
			option_model = models.Option.objects.get(code=option)
			cars = cars.filter(options=option_model)
		found_cars = []
		recommended_cars = []
		count_found = 0
		for car in cars:
			if(len(car.options.all())==len(options)):
				count_found = count_found + 1
				found_cars.append(car)
			else:
				recommended_cars.append(car)

		serializer1 = self.get_serializer(found_cars, many=True)
		serializer2 = self.get_serializer(recommended_cars, many=True)
		return Response(
			{
				"count_found": count_found,
				"found_cars": serializer1.data,
				"recommended_cars": serializer2.data
			}, 
			status=status.HTTP_200_OK)
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def login_facebook(request):
	"""Function for login and register
	:return:token for authorization or error
	"""
	data = json.loads(request.body.decode('utf-8'))
	access_token = data.get('accessToken')
	new_user = False
	try:
		graph = facebook.GraphAPI(access_token=access_token)
		user_info = graph.get_object(
		id='me',
		fields='first_name, middle_name, last_name, id, '
		'currency, hometown, location, locale, '
		'email, gender, interested_in, picture.type(large),'
		' birthday, cover')
	except facebook.GraphAPIError:
		return JsonResponse({'error': 'Invalid data'}, safe=False)

	try:
		user = models.Automobilist.objects.get(facebook_id=user_info.get('id'))

	except models.Automobilist.DoesNotExist:
		password = models.Automobilist.objects.make_random_password()
		user = models.Automobilist(
			first_name=user_info.get('first_name'),
			last_name=user_info.get('last_name'),
			email=user_info.get('email')
			or '{0} without email'.format(user_info.get('last_name')),
			facebook_id=user_info.get('id'),
			profile_image=user_info.get('picture')['data']['url'],
			address= user_info.get('hometown') or "",
			#date_joined=datetime.now(),
			username=user_info.get('email') or user_info.get('last_name'),
			gender= user_info.get('gender') or "",
			#is_active=1
		)
		user.set_password(password)
		user.save()
		new_user = True
	token, created  = Token.objects.get_or_create(user=user)
	if token:
		return JsonResponse({'auth_token': token.key, 'new_automobilist': new_user, 'automobilist_id': user.id},
	                safe=False)
	else:
		return JsonResponse({'error': 'Invalid data'}, safe=False)


@csrf_exempt
def login_google(request):

	requestJson = json.loads(request.body)
	request = requests.Request()

	id_info = id_token.verify_oauth2_token(requestJson['accessToken'], request, "627073783203-91jqscu6j71of3hulleeftckl0iuvec7.apps.googleusercontent.com")

	if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
		return Response("Unable to Validate User: Wrong Issuer")
		# raise ValueError('Wrong issuer.')

	if not id_info:
		return Response("Unable to Validate User: Invalid Token")
		# raise Exception("Unable to Validate Token")

	id = id_info['email']

	new_user = False
	try:
		user = models.Automobilist.objects.get(email=id)

	except models.Automobilist.DoesNotExist:
		password = models.Automobilist.objects.make_random_password()
		user = models.Automobilist(
			email=id,
			first_name= id_info['given_name'] or "",
			last_name= id_info['family_name'] or "",
			address= id_info['locale'] or "",
			profile_image=  id_info['picture'] or "",
			facebook_id="",
			username= id_info['given_name'] + " " + id_info['family_name'],
			gender= ""
		)
		user.set_password(password)
		user.save()
		new_user = True
	token, created  = Token.objects.get_or_create(user=user)

	if token:

		return JsonResponse({'auth_token': token.key, 'new_automobilist': new_user, 'automobilist_id': user.id},
	                safe=False)
	else:
		return JsonResponse({'error': 'Invalid data'}, safe=False)


"""
FollowedModelsViewSet : get (read only endpoint) paginated output
"""
class AutomobilistNotificationViewSet(ListAPIView):

	#permission_classes = (IsAuthenticated,)  
	serializer_class = serializers.AutomobilistNotificationSerializer

	def get_queryset(self, recipient):

		try:
			return models.AutomobilistNotification.objects.filter(recipient = recipient)

		except models.AutomobilistNotification.DoesNotExist:

			raise Http404

	def list(self, request,*kwargs, recipient):
		queryset = self.get_queryset(recipient)
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response(data)


"""
FollowedModelsViewSet : get (read only endpoint) paginated output
"""
class AutomobilistNotificationCrudView(viewsets.ModelViewSet):

	#permission_classes = (IsAuthenticated,)  
	serializer_class = serializers.AutomobilistNotificationSerializer 
	queryset = models.AutomobilistNotification.objects.all()
	