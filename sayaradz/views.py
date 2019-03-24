import django_filters
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import logout
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from sayaradz_api import serializers 
from sayaradz import models
from rest_framework import status
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveDestroyAPIView, GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView


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
	permission_classes = (IsAuthenticated,)  
	queryset = models.ManufacturerUser.objects.all()
	serializer_class = serializers.ManufacturerUserSerializer

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

"""
AdminLoginAPIView : post only, allows admin authentification
"""
class AdminLoginAPIView(GenericAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.AdminLoginSerializer
	
	def post(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			
			user = serializer.user
			if user.is_superuser:
				token, _ = Token.objects.get_or_create(user=user)

				return Response(
					data=serializers.TokenSerializer(token).data,
					status=status.HTTP_200_OK,
				)
			else:
				return Response(
				data="Login Failed",
				status=status.HTTP_400_BAD_REQUEST,
				)
			

			return Response(
				data=TokenSerializer(token).data,
				status=status.HTTP_200_OK,
			)

		else:
			
			return Response(
				data=serializer.errors,
				status=status.HTTP_400_BAD_REQUEST,
			)

"""
ManufacturerUserLoginAPIView : post only, allows manufacturer user authentification
"""
class ManufacturerUserLoginAPIView(GenericAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.ManufacturerUserLoginSerializer
	
	def post(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():

			user = serializer.user
			if not user.is_superuser:
				if not user.is_blocked:
					token, _ = Token.objects.get_or_create(user=user)

					return Response(
						data=serializers.TokenSerializer(token).data,
						status=status.HTTP_200_OK,
					)
				else:
					return Response(
						data="Blocked",
						status=status.HTTP_400_BAD_REQUEST,
					)

			else:
				return Response(
				data="Login Failed",
				status=status.HTTP_400_BAD_REQUEST,
				)

		else:
			return Response(
				data=serializer.errors,
				status=status.HTTP_400_BAD_REQUEST,
			)

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
LogoutView : post only, allows users logout
"""
class LogoutView(GenericAPIView):

	serializer_class = serializers.ManufacturerUserLoginSerializer
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

"""
ColorViewSet : get, delete, patch, partial_update, put, paginated output
"""
class ColorViewSet(viewsets.ModelViewSet):

	pagination_class = StandardResultsSetPagination
	permission_classes = (IsAuthenticated,)  
	queryset = models.Color.objects.all().prefetch_related('options')
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

"""
AutomobilistMyModelViewSet : get (read only endpoint) paginated output
"""
class AutomobilistMyModelViewSet(ListAPIView):

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
		return Response(data)

"""
AutomobilistVersionViewSet : get (Read only endpoint) paginated output
"""
class AutomobilistVersionViewSet(ListAPIView):

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
		return Response(data)



"""
AutomobilistViewSet1
"""
class AutomobilistViewSet1(mixins.UpdateModelMixin, viewsets.GenericViewSet):

	queryset = models.Automobilist.objects.all().prefetch_related('followedModels').prefetch_related('followedVersions')
	http_method_names = ('put', 'patch')
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

"""
LigneTarifOptionViewSet
"""
class LigneTarifOptionViewSet(viewsets.ModelViewSet):

    queryset = models.LigneTarifOption.objects.all()

    serializer_class = serializers.LigneTarifOptionSerializer

"""
LigneTarifColorViewSet
"""
class LigneTarifColorViewSet(viewsets.ModelViewSet):

    queryset = models.LigneTarifColor.objects.all()

    serializer_class = serializers.LigneTarifOptionSerializer

"""
NewCarViewSet
"""
class NewCarViewSet(viewsets.ModelViewSet):

    queryset = models.NewCar.objects.all()
    serializer_class = serializers.NewCarSerializer

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
	class Meta:
		model = models.NewCar
		fields = ['numChassis', 'color','version', 'options', 'color__name']

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
		fields = ['id','model', 'model__name', 'version', 'version__name', 'manufacturer', 'manufacturer__name', 'minPrice', 'date', 'automobilist', 'automobilist__firstName', 'automobilist__familyName']

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
	search_fields = ('model', 'model__name', 'version', 'version__name', 'manufacturer__name', 'minPrice', 'date', 'automobilist__firstName', 'automobilist__familyName')
	ordering_fields = '__all__'

"""
AutomobilistMyModelViewSet : get (read only endpoint) paginated output
"""
class AdViewSet(viewsets.ModelViewSet):

	pagination_class = StandardResultsSetPagination
	permission_classes = (IsAuthenticated,)  
	queryset = models.Ad.objects.all()
	serializer_class = serializers.MyModelSerializer

	def list(self, request,*kwargs):
		queryset = models.Ad.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

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


"""
AdOfferGetView : Get ad offers
"""
class AdOfferGetView(APIView):

	def get_object(self, ad):
		
		try:
			
			return models.Offer.objects.filter(ad=ad)

		except models.Offer.DoesNotExist:

			raise Http404

	def get(self, request, ad, format=None):

		data = self.get_object(ad)
		return Response(data)

"""
AutomobilistOfferGetView : Get automobilist offers
"""
class AutomobilistOfferGetView(APIView):

	def get_object(self, automobilist):
		
		try:
			
			return models.Offer.objects.filter(automobilist=automobilist)

		except models.Offer.DoesNotExist:

			raise Http404

	def get(self, request, automobilist, format=None):

		data = self.get_object(automobilist)
		return Response(data)

"""
OfferUpdateView : Poster une annonce
"""
class OfferUpdateView(UpdateAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = serializers.OfferSerializer

	




	







	
	