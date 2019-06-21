from django.shortcuts import render
#from rest_framework import viewsets
from rest_framework import routers, serializers, viewsets, permissions
from .models import Language
from .serializers import LanguageSerializer 
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    posts=['amira','hadjer']
    return render(request,'index.html',{'posts':posts})

class LanguageView(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

