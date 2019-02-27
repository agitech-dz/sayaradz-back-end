from django.shortcuts import render

from rest_framework import routers, serializers, viewsets

from rest_framework.permissions import IsAuthenticated

from sayaradz_api.serializers import UserSerializer, MakeSerializer, MakeUserSerializer, AdminLoginSerializer, MakeUserLoginSerializer, TokenSerializer


from sayaradz.models import Make, MakeUser, MyUser

from rest_framework import status

from rest_framework.authtoken.models import Token

from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveDestroyAPIView

from rest_framework.response import Response



# Create your views here.

# ViewSets define the view behavior.

class UserViewSet(viewsets.ModelViewSet):

    queryset = MyUser.objects.all()

    serializer_class = UserSerializer



# ViewSets define the view behavior.

class MakeViewSet(viewsets.ModelViewSet):

	#permission_classes = (IsAuthenticated,)  

	queryset = Make.objects.all()

	serializer_class = MakeSerializer

# ViewSets define the view behavior.

class MakeUserViewSet(viewsets.ModelViewSet):

    queryset = MakeUser.objects.all().select_related('user')

    serializer_class = MakeUserSerializer

class AdminLoginAPIView(ListCreateAPIView):

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


class MakeUserLoginAPIView(ListCreateAPIView):

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