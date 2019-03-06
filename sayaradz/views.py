import django_filters
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import logout
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from sayaradz_api.serializers import AdminRegistrationSerializer, ManufacturerUserRegistrationSerializer, AdminSerializer, ManufacturerSerializer, ManufacturerUserSerializer, AdminLoginSerializer, ManufacturerUserLoginSerializer, TokenSerializer, MyModelSerializer, VersionSerializer, OptionSerializer
from sayaradz.models import Manufacturer, ManufacturerUser, MyModel, Version, Option
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User


"""
UserViewSet
"""
class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()

    serializer_class = AdminSerializer

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

	queryset = Manufacturer.objects.all()
	serializer_class = ManufacturerSerializer
	#filter_backends = (DjangoFilterBackend,)
	#filter_fields = ('name', 'nationality')
	def list(self, request,*kwargs):
		queryset = Manufacturer.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		count = Manufacturer.objects.all().count()
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
	queryset = ManufacturerUser.objects.all()
	serializer_class = ManufacturerUserSerializer

	def list(self, request,*kwargs):
		queryset = ManufacturerUser.objects.all()
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		count1 = ManufacturerUser.objects.all().count()
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
	serializer_class = AdminRegistrationSerializer

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
	serializer_class = ManufacturerUserRegistrationSerializer

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
	serializer_class = AdminLoginSerializer
	
	def post(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			
			user = serializer.user
			if user.is_superuser:
				token, _ = Token.objects.get_or_create(user=user)

				return Response(
					data=TokenSerializer(token).data,
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
	serializer_class = ManufacturerUserLoginSerializer
	
	def post(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():

			user = serializer.user
			if not user.is_superuser:
				if not user.is_blocked:
					token, _ = Token.objects.get_or_create(user=user)

					return Response(
						data=TokenSerializer(token).data,
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
	serializer_class = TokenSerializer
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

	serializer_class = ManufacturerUserLoginSerializer
	def post(self, request):

		django_logout(request)
		return Response(status=204)

"""
ManufacturerUserFilter : filter ManufacturerUser output data by ['address', 'first_name','manufacturer', 'manufacturer__name']
"""
class ManufacturerUserFilter(django_filters.FilterSet):
	class Meta:
		model = ManufacturerUser
		fields = ['address', 'first_name','manufacturer', 'manufacturer__name']

"""
ManufacturerUserList : Get only, allows to get ManufacturerUser output data 
 : using  	filtering by ['address', 'first_name','manufacturer', 'manufacturer__name'],
			Search
			ordering
"""
class ManufacturerUserList(ListAPIView):
	permission_classes = (IsAuthenticated,)  
	queryset = ManufacturerUser.objects.all()
	serializer_class = ManufacturerUserSerializer
	filter_class = ManufacturerUserFilter
	filter_backends = (filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend,)
	search_fields = ('username', 'email', 'address', 'manufacturer__name')
	ordering_fields = '__all__'
	

"""
ManufacturerUserFilter : filter ManufacturerUser output data by ['id', 'name', 'nationality']
"""
class ManufacturerFilter(django_filters.FilterSet):
	class Meta:
		model = Manufacturer
		fields = ['id', 'name', 'nationality']

"""
ManufacturerList : Get only, allows to get Manufacturer output data 
 : using  	filtering by ['address', 'first_name','manufacturer', 'manufacturer__name'],
			Search
			ordering
"""
class ManufacturerList(ListAPIView):
	
	permission_classes = (IsAuthenticated,)  
	queryset = Manufacturer.objects.all()

	serializer_class = ManufacturerSerializer
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
	queryset = MyModel.objects.all()
	serializer_class = MyModelSerializer

	def list(self, request,*kwargs):
		queryset = MyModel.objects.all()
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
		model = MyModel
		fields = ['code', 'name', 'manufacturer', 'manufacturer__name']

"""
MyModelList : Get only, allows to get ManufacturerUser output data 
 : using  	filtering by ['code', 'name', 'manufacturer__name'],
			Search
			ordering
"""
class MyModelList(ListAPIView):

	permission_classes = (IsAuthenticated,)  
	queryset = MyModel.objects.all()
	serializer_class = MyModelSerializer
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
	queryset = Option.objects.all()
	serializer_class = OptionSerializer

"""
VersionViewSet : get, delete, patch, partial_update, put, paginated output
"""
class VersionViewSet(viewsets.ModelViewSet):

	#pagination_class = StandardResultsSetPagination
	

	permission_classes = (IsAuthenticated,)  
	queryset = Version.objects.all().prefetch_related('options')
	serializer_class = VersionSerializer

	
	