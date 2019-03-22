from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from sayaradz import models
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password

"""
AdminSerializer : defines Admin model representation
feilds : ('username', 'email', 'first_name', 'last_name', 'password' , 'is_superuser')
"""
class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password' , 'is_superuser')

"""
ManufacturerSerializer : defines Manufacturer model representation
feilds : ('id','name', 'nationality')
"""
class ManufacturerSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = models.Manufacturer
		fields = ('id','name', 'nationality')

"""
ManufacturerUserSerializer : defines ManufacturerUser model representation
feilds : ('id','username','first_name', 'last_name',  'address', 'telephone', 'manufacturer', 'email', 'is_active')
"""
class ManufacturerUserSerializer(serializers.ModelSerializer):
	manufacturer_name = serializers.ReadOnlyField(source='manufacturer.name') 

	class Meta:
		model = models.ManufacturerUser
		fields = ('id','username','first_name', 'last_name',  'address', 'telephone', 'email', 'is_blocked', 'manufacturer', 'manufacturer_name')

"""
AdminRegistrationSerializer : defines required Admin registration feilds  
feilds : ("id",'first_name', 'last_name', "username", "password", "confirm_password")
"""
class AdminRegistrationSerializer(serializers.ModelSerializer):

	confirm_password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ("id",'first_name', 'last_name', "username", "password", "confirm_password")
	
	def create(self, validated_data):

		del validated_data["confirm_password"]
		validated_data["password"] = make_password(validated_data['password'])
		return super(AdminRegistrationSerializer, self).create(validated_data)

	def validate(self, attrs):

		if attrs.get('password') != attrs.get('confirm_password'):
			raise serializers.ValidationError("Those passwords don't match.")
		return attrs

"""
AdminLoginSerializer : defines required Admin Login feilds  
feilds : ("username", "password")
"""
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

"""
TokenSerializer : defines Token Model presentation  
feilds : ("auth_token", "created", "user_id")
"""
class TokenSerializer(serializers.ModelSerializer):
	auth_token = serializers.CharField(source='key')
	class Meta:
		model = Token
		fields = ("auth_token", "created", "user")

"""
ManufacturerUserRegistrationSerializer : defines required ManufacturerUser registration feilds  
feilds : ("id", "username","first_name","last_name", "password", "confirm_password","manufacturer", "address", "telephone", "is_active")
"""
class ManufacturerUserRegistrationSerializer(serializers.ModelSerializer):

	confirm_password = serializers.CharField(write_only=True)

	class Meta:
		model = models.ManufacturerUser
		fields = ("id", "username","first_name","last_name", "password", "confirm_password","manufacturer", "address", "telephone", 'is_blocked')
	
	def create(self, validated_data):

		del validated_data["confirm_password"]
		validated_data["password"] = make_password(validated_data['password'])
		
		return super(ManufacturerUserRegistrationSerializer, self).create(validated_data)

	def validate(self, attrs):

		if attrs.get('password') != attrs.get('confirm_password'):
			raise serializers.ValidationError("Those passwords don't match.")
		return attrs

"""
ManufacturerUserLoginSerializer : defines required ManufacturerUser Login feilds  
feilds : ("username", "password")
"""
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

"""
ModelSerializer : defines Manufacturer model representation
feilds : ('code','name', 'manufacturer', 'manufacturer_name')
"""
class MyModelSerializer(serializers.ModelSerializer):

	manufacturer_name = serializers.ReadOnlyField(source='manufacturer.name') 
	class Meta:
		model = models.MyModel
		fields = ('code','name', 'manufacturer', 'manufacturer_name')

"""
OptionSerializer : defines Option model representation
feilds : ('code','name', 'model', 'model_name')
"""
class OptionSerializer(serializers.ModelSerializer):

	model_name = serializers.ReadOnlyField(source='model.name') 
	manufacturer = serializers.ReadOnlyField(source='model.manufacturer_id') 
	class Meta:
		model = models.Option
		fields = ('code','name', 'model', 'model_name', 'manufacturer')

"""
VersionSerializer : defines Version model representation
fields = ('code','name', 'options', 'model')
"""
class VersionSerializer(serializers.ModelSerializer):

	options = serializers.PrimaryKeyRelatedField(required=True, many=True, read_only=False, queryset=models.Option.objects.all()) 

	class Meta:
		model = models.Version
		fields = ('code','name', 'options', 'model')

"""
ColorSerializer : defines Color model representation
fields = ('code','name', 'manufacturer')
"""
class ColorSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Color
		fields = ('code','name', 'model')

"""
AutomobilistSerializer1 : defines Automobilist model representation follow
fields = ('id', 'followedModels', 'followedVersions')
"""
class AutomobilistSerializer1(serializers.ModelSerializer):

	followedModels = serializers.PrimaryKeyRelatedField(required=True, many=True, read_only=False, queryset=models.MyModel.objects.all()) 
	followedVersions = serializers.PrimaryKeyRelatedField(required=True, many=True, read_only=False, queryset=models.Version.objects.all()) 

	class Meta:
		model = models.Automobilist
		fields = ('id', 'followedModels', 'followedVersions')

	def update(self, instance, validated_data):

		followedModels = validated_data.pop('followedModels', None)
		followedVersions= validated_data.pop('followedVersions', None)
		instance = super().update(instance, validated_data) # if you want to update other fields

		# now add new followed Models 
		if followedModels is not None:
			for followedModel in followedModels:
				instance.followedModels.add(followedModel)

		# now add new followed Versions 
		if followedVersions is not None:
			for followedVersion in followedVersions:
				instance.followedVersions.add(followedVersion)

		instance.save()

		return instance

"""
AutomobilistSerializer2 : defines Automobilist model representation unfollow
fields = ('id', 'followedModels', 'followedVersions')
"""
class AutomobilistSerializer2(serializers.ModelSerializer):

	id = serializers.CharField(source='automobilist')
	followedModels = serializers.PrimaryKeyRelatedField(required=True, many=True, read_only=False, queryset=models.MyModel.objects.all()) 
	followedVersions = serializers.PrimaryKeyRelatedField(required=True, many=True, read_only=False, queryset=models.Version.objects.all()) 

	class Meta:
		model = models.Automobilist
		fields = ('id', 'followedModels', 'followedVersions')

	def update(self, instance, validated_data):

		followedModels = validated_data.pop('followedModels', None)
		followedVersions= validated_data.pop('followedVersions', None)
		instance = super().update(instance, validated_data) # if you want to update other fields

		# now add new followed Models 
		if followedModels is not None:
			for followedModel in followedModels:
				instance.followedModels.remove(followedModel)

		# now add new followed Versions 
		if followedVersions is not None:
			for followedVersion in followedVersions:
				instance.followedVersions.remove(followedVersion)

		instance.save()

		return instance

"""
LigneTarifVersionSerializer : defines LigneTarifVersion model representation
fields = ('code','name', 'manufacturer')
"""
class LigneTarifVersionSerializer(serializers.ModelSerializer):

	#version = VersionSerializer(read_only = True)

	class Meta:
		model = models.LigneTarifVersion
		fields = ('id', 'code','dateBegin', 'dateEnd', 'price')

"""
LigneTarifOptionSerializer : defines LigneTarifVersion model representation
fields = ('code','name', 'manufacturer')
"""
class LigneTarifOptionSerializer(serializers.ModelSerializer):

	#version = VersionSerializer(read_only = True)

	class Meta:
		model = models.LigneTarifOption
		fields = ('id', 'code','dateBegin', 'dateEnd', 'price')
