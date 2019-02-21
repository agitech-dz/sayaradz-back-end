from django.shortcuts import render

from rest_framework import routers, serializers, viewsets

from sayaradz_api.serializers import UserSerializer, MakeSerializer, MakeUserSerializer

from django.contrib.auth.models import User

from sayaradz.models import Make, MakeUser

# Create your views here.

# ViewSets define the view behavior.

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()

    serializer_class = UserSerializer



# ViewSets define the view behavior.

class MakeViewSet(viewsets.ModelViewSet):

    queryset = Make.objects.all()

    serializer_class = MakeSerializer





# ViewSets define the view behavior.

class MakeUserViewSet(viewsets.ModelViewSet):

    queryset = MakeUser.objects.all()

    serializer_class = MakeUserSerializer