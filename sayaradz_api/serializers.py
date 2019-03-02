from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from sayaradz.models import Manufacturer, ManufacturerUser
from django.contrib.auth.models import User 

from django.contrib.auth.hashers import make_password


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password' , 'is_superuser')


# Serializers define the API representation.
class ManufacturerSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Manufacturer
		fields = ('id','name', 'nationality')


# Serializers define the API representation.
class ManufacturerUserSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ManufacturerUser
		fields = ('id','username','first_name', 'last_name',  'address', 'telephone', 'manufacturer', 'email', 'is_active')

class UserRegistrationSerializer(serializers.ModelSerializer):

	confirm_password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ("id",'first_name', 'last_name', 'address', 'telephone', "username", "password", "confirm_password")
	

	def create(self, validated_data):
		del validated_data["confirm_password"]
		validated_data["password"] = make_password(validated_data['password'])
		
		return super(UserRegistrationSerializer, self).create(validated_data)

	def validate(self, attrs):
		if attrs.get('password') != attrs.get('confirm_password'):
			raise serializers.ValidationError("Those passwords don't match.")
		return attrs



class AdminLoginSerializer(serializers.Serializer):

	username = serializers.CharField(required=True)
	password = serializers.CharField(required=True)

	default_error_messages = {
		'inactive_account': _('User account is disabled.'),
		'invalid_credentials': _('Unable to login with provided credentials.')
	}

	def __init__(self, *args, **kwargs):

		super(AdminLoginSerializer, self).__init__(*args, **kwargs)
		self.user = None


	def validate(self, attrs):
		self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
		if self.user:

			if not self.user.is_active:
				raise serializers.ValidationError(self.error_messages['inactive_account'])
			return attrs

		else:
			raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class TokenSerializer(serializers.ModelSerializer):
	auth_token = serializers.CharField(source='key')
	class Meta:
		model = Token
		fields = ("auth_token", "created", "user")


class ManufacturerUserRegistrationSerializer(serializers.ModelSerializer):

	confirm_password = serializers.CharField(write_only=True)
	class Meta:
		model = ManufacturerUser
		fields = ("id", "username", "password", "confirm_password","manufacturer", "address")
	

	def create(self, validated_data):
		del validated_data["confirm_password"]
		validated_data["password"] = make_password(validated_data['password'])
		
		return super(ManufacturerUserRegistrationSerializer, self).create(validated_data)

	def validate(self, attrs):
		if attrs.get('password') != attrs.get('confirm_password'):
			raise serializers.ValidationError("Those passwords don't match.")
		return attrs



class ManufacturerUserLoginSerializer(serializers.Serializer):

	username = serializers.CharField(required=True)
	password = serializers.CharField(required=True)

	default_error_messages = {
		'inactive_account': _('User account is disabled.'),
		'invalid_credentials': _('Unable to login with provided credentials.')
	}

	def __init__(self, *args, **kwargs):
		super(ManufacturerUserLoginSerializer, self).__init__(*args, **kwargs)
		self.user = None

	def validate(self, attrs):

		self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
		if self.user:

			if not self.user.is_active:
				raise serializers.ValidationError(self.error_messages['inactive_account'])

			return attrs

		else:
			raise serializers.ValidationError(self.error_messages['invalid_credentials'])
