import django_filters
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.contrib.auth import logout

from django.shortcuts import render

from rest_framework import routers, serializers, viewsets

from rest_framework.permissions import IsAuthenticated

from sayaradz_api.serializers import UserRegistrationSerializer, ManufacturerUserRegistrationSerializer, UserSerializer, ManufacturerSerializer, ManufacturerUserSerializer, AdminLoginSerializer, ManufacturerUserLoginSerializer, TokenSerializer

from sayaradz.models import Manufacturer, ManufacturerUser

from rest_framework import status

from rest_framework.authtoken.models import Token

from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveDestroyAPIView, GenericAPIView

from rest_framework.response import Response

from django.contrib.auth.models import User


# Create your views here.

# ViewSets define the view behavior.

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()

    serializer_class = UserSerializer



# ViewSets define the view behavior.

class ManufacturerViewSet(viewsets.ModelViewSet):

	#permission_classes = (IsAuthenticated,)  

	queryset = Manufacturer.objects.all()
	serializer_class = ManufacturerSerializer
	#filter_backends = (DjangoFilterBackend,)
	#filter_fields = ('name', 'nationality')
	def list(self, request,*kwargs):
		queryset = Manufacturer.objects.all()
		count = Manufacturer.objects.all().count()
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data
		return Response({
			'data':data,
			'meta':{
				'total':count
				},
			})



# ViewSets define the view behavior.

class ManufacturerUserViewSet(viewsets.ModelViewSet):

	queryset = ManufacturerUser.objects.select_related('manufacturer').all()

	serializer_class = ManufacturerUserSerializer

	#filter_backends = (DjangoFilterBackend,)
	#filter_fields = ('manufacturer', 'address', 'first_name')

	def list(self, request,*kwargs):
		queryset = ManufacturerUser.objects.select_related('manufacturer').all()

		count = ManufacturerUser.objects.all().count()
		serializer = self.get_serializer(queryset,many=True)
		data = serializer.data

		return Response({
			'data':data,
			'meta':{
				'total':count
				},
			})

class UserRegistrationAPIView(CreateAPIView):
	authentication_classes = ()
	permission_classes = ()
	serializer_class = UserRegistrationSerializer

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

class AdminLoginAPIView(GenericAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = AdminLoginSerializer
	
	def post(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			
			user = serializer.user

			token, _ = Token.objects.get_or_create(user=user)

			return Response(
				data=TokenSerializer(token).data,
				status=status.HTTP_200_OK,
			)

		else:
			
			return Response(
				data=serializer.errors,
				status=status.HTTP_400_BAD_REQUEST,
			)


class ManufacturerUserLoginAPIView(GenericAPIView):

	authentication_classes = ()
	permission_classes = ()
	serializer_class = ManufacturerUserLoginSerializer
	
	def post(self, request, *args, **kwargs):

		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():

			user = serializer.user
			if not user.is_superuser:
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


class LogoutView(GenericAPIView):

	def post(self, request):

		django_logout(request)
		return Response(status=204)


class ManufacturerUserFilter(django_filters.FilterSet):
	class Meta:
		model = ManufacturerUser
		fields = ['address', 'first_name','manufacturer', 'manufacturer__name']

class ManufacturerUserList(ListAPIView):
	queryset = ManufacturerUser.objects.all()
	serializer_class = ManufacturerUserSerializer
	filter_class = ManufacturerUserFilter
	filter_backends = (filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend,)
	search_fields = ('username', 'email', 'address', 'manufacturer__name')
	ordering_fields = '__all__'


class ManufacturerFilter(django_filters.FilterSet):
	class Meta:
		model = Manufacturer
		fields = ['name', 'nationality']

class ManufacturerList(ListAPIView):
	queryset = Manufacturer.objects.all()
	serializer_class = ManufacturerSerializer
	filter_class = ManufacturerFilter
	filter_backends = (filters.SearchFilter, filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend,)
	search_fields = ('name', 'nationality')	
	ordering_fields = '__all__'