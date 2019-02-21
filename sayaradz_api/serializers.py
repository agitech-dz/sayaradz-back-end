from rest_framework import serializers

from django.contrib.auth.models import User
from sayaradz.models import Make, MakeUser

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# Serializers define the API representation.
class MakeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Make
        fields = ('id','name')

# Serializers define the API representation.
class MakeUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MakeUser
        fields = ('id','email', 'firstName','familyName','password', 'address', 'telephone','isBlocked', 'make')