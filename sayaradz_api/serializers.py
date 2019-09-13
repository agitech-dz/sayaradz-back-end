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
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password' , 'is_superuser')

"""
ManufacturerSerializer : defines Manufacturer model representation
feilds : ('id','name', 'nationality')
"""
class ManufacturerSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = models.Manufacturer
		fields = ('id','name', 'nationality', 'image')

"""
ManufacturerUserSerializer : defines ManufacturerUser model representation
feilds : ('id','username','first_name', 'last_name',  'address', 'telephone', 'manufacturer', 'email', 'is_active')
"""
class ManufacturerUserSerializer(serializers.ModelSerializer):
	manufacturer_name = serializers.ReadOnlyField(source='manufacturer.name') 

	class Meta:
		model = models.ManufacturerUser
		fields = ('id','username','first_name', 'last_name','password', 'address', 'telephone', 'email', 'is_blocked', 'manufacturer', 'manufacturer_name')

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
class UserLoginSerializer(serializers.Serializer):

	username = serializers.CharField(required=True)
	password = serializers.CharField(required=True)

	default_error_messages = {
		'inactive_account': _('User account is disabled.'),
		'invalid_credentials': _('Unable to login with provided credentials.')
	}

	def __init__(self, *args, **kwargs):

		super(UserLoginSerializer, self).__init__(*args, **kwargs)
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
	is_superuser = serializers.ReadOnlyField(source='user.is_superuser')
	class Meta:
		model = Token
		fields = ("auth_token", "created", "user", "is_superuser")

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
ModelSerializer : defines Manufacturer model representation
feilds : ('code','name', 'manufacturer', 'manufacturer_name')
"""
class MyModelSerializer(serializers.ModelSerializer):

	manufacturer_name = serializers.ReadOnlyField(source='manufacturer.name') 
	id = serializers.CharField(source='code')
	class Meta:
		model = models.MyModel
		fields = ('id','name', 'manufacturer', 'manufacturer_name', 'image')

"""
OptionSerializer : defines Option model representation
feilds : ('code','name', 'model', 'model_name')
"""
class OptionSerializer(serializers.ModelSerializer):

	model_name = serializers.ReadOnlyField(source='model.name') 
	manufacturer = serializers.ReadOnlyField(source='model.manufacturer_id') 
	tarif_id = serializers.ReadOnlyField(source='lignetarifoption.id')
	tarif_price = serializers.ReadOnlyField(source='lignetarifoption.price')
	tarif_date_begin = serializers.ReadOnlyField(source='lignetarifoption.datebegin')
	tarif_date_end = serializers.ReadOnlyField(source='lignetarifoption.dateend') 
	id = serializers.CharField(source='code')

	class Meta:
		model = models.Option
		fields = ('id','name', 'model', 'model_name', 'manufacturer', 'tarif_id', 'tarif_price', 'tarif_date_begin', 'tarif_date_end')

"""
VersionSerializer : defines Version model representation
fields = ('code','name', 'options', 'model')
"""
class VersionSerializer(serializers.ModelSerializer):

	options = serializers.PrimaryKeyRelatedField(required=True, many=True, read_only=False, queryset=models.Option.objects.all()) 
	tarif_id = serializers.ReadOnlyField(source='lignetarifversion.id')
	tarif_price = serializers.ReadOnlyField(source='lignetarifversion.price')
	tarif_date_begin = serializers.ReadOnlyField(source='lignetarifversion.datebegin')
	tarif_date_end = serializers.ReadOnlyField(source='lignetarifversion.dateend') 
	id = serializers.CharField(source='code')
	class Meta:
		model = models.Version
		fields = ('id','name', 'options', 'model', 'image', 'tarif_id', 'tarif_price', 'tarif_date_begin', 'tarif_date_end')


"""
ColorSerializer : defines Color model representation
fields = ('code','name', 'manufacturer')
"""
class ColorSerializer(serializers.ModelSerializer):

	tarif_id = serializers.ReadOnlyField(source='lignetarifcolor.id')
	tarif_price = serializers.ReadOnlyField(source='lignetarifcolor.price')
	tarif_date_begin = serializers.ReadOnlyField(source='lignetarifcolor.datebegin')
	tarif_date_end = serializers.ReadOnlyField(source='lignetarifcolor.dateend') 
	id = serializers.CharField(source='code')
	class Meta:
		model = models.Color
		fields = ('id','name', 'model', 'tarif_id', 'tarif_price', 'tarif_date_begin', 'tarif_date_end')

"""
AutomobilistSerializer : defines Automobilist model representation follow
fields = ('firstName', 'familyName', 'password', 'address', 'telephone', 'avatar')
"""
class AutomobilistSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Automobilist
		fields = ('id', 'first_name', 'last_name', "username", "password", 'address', 'telephone', 'profile_image')

"""
AutomobilistSerializer1 : defines Automobilist model representation follow
fields = ('id', 'followedModels', 'followedVersions')
"""
class AutomobilistSerializer1(serializers.ModelSerializer):

	followedModels = ""
	followedVersions = ""

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
	followedModels = ""
	followedVersions = ""

	class Meta:
		model = models.Automobilist
		fields = ('id')

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
LigneTarifSerializer : defines LigneTarifmodel representation
fields = ('id', 'code','dateBegin', 'dateEnd', 'price')
"""
class LigneTarifSerializer(serializers.ModelSerializer):

	#version = VersionSerializer(read_only = True)

	class Meta:
		model = models.LigneTarif
		fields = ('id','dateBegin', 'dateEnd', 'price')

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

"""
LigneTarifColorSerializer : defines LigneTarifVersion model representation
fields = ('code','name', 'manufacturer')
"""
class LigneTarifColorSerializer(serializers.ModelSerializer):

	#version = VersionSerializer(read_only = True)

	class Meta:
		model = models.LigneTarifColor
		fields = ('id', 'code','dateBegin', 'dateEnd', 'price')

class NewCarSerializer(serializers.ModelSerializer):

	#version = VersionSerializer(read_only = True)
	options = serializers.PrimaryKeyRelatedField(required=True, many=True, read_only=False, queryset=models.Option.objects.all()) 
	id = serializers.CharField(source='numChassis')
	class Meta:
		model = models.NewCar
		fields = ('id', 'color','version', 'options', 'seller', 'isExisted')

"""
AdSerializer : defines Ad (Annonce) model representation
fields = ('id','model', 'model_name', 'version', 'version_name', 'manufacturer', 'manufacturer_name', 'photo1', 'photo2', 'photo3', 'minPrice', 'date', 'automobilist', 'automobilist_firstName', 'automobilist_familyName')
"""
class AdSerializer(serializers.ModelSerializer):

	model_name = serializers.ReadOnlyField(source='mymodel.name') 
	manufacturer_name = serializers.ReadOnlyField(source='manufacturer.name') 
	version_name = serializers.ReadOnlyField(source='version.name') 
	automobilist_username = serializers.ReadOnlyField(source='automobilist.username') 
	automobilist_address = serializers.ReadOnlyField(source='automobilist.address') 
	#version = serializers.ReadOnlyField(source='version.code') 


	class Meta:
		model = models.Ad
		fields = ('id','model', 'model_name', 'version', 'version_name', 'manufacturer', 'manufacturer_name', 'year', 'distance', 'description', 'photo1', 'photo2', 'photo3', 'minPrice', 'date', 'automobilist', 'automobilist_username', 'automobilist_address')

"""
OfferSerializer : defines Ad (Annonce) model representation
fields = ('id', 'ad', 'offredAmount', 'automobilist', 'automobilist_firstName', 'automobilist_familyName', 'date', 'isAccepted')
"""
class OfferSerializer(serializers.ModelSerializer):
 
	automobilist_userName = serializers.ReadOnlyField(source='automobilist.username') 

	class Meta:
		model = models.Offer
		fields = ('id','ad', 'offredPrice', 'automobilist', 'automobilist_userName', 'date', 'isAccepted')

"""
AutomobilistOfferAcceptNotificationSerializer : defines AutomobilistOfferAcceptNotification model representation
feilds : ('id', 'actor','action_object', 'recepient', 'verb','target')
	actor: sender(Automobilist_id ad owner)
	action_objet: offerId
	recepient: offer owner
	verb: offeredPrice
	target: ad id
"""
class AutomobilistAcceptOfferNotificationSerializer(serializers.ModelSerializer):

	actorUserName = serializers.ReadOnlyField(source='actor.username') 
	actorEmail = serializers.ReadOnlyField(source='actor.email')
	actorTelephone = serializers.ReadOnlyField(source='actor.telephone')  
	actor = serializers.CharField(source='actor_object_id')
	actorTarget = serializers.CharField(source='target_object_id') #ad id

	class Meta:
		model = models.AutomobilistAcceptOfferNotification
		fields = ('id', 'offer', 'actor', 'actorUserName','actorEmail', 'actorTelephone', 'actorTarget', 'recipient', 'verb', 'timestamp', 'unread', 'notification_type')

"""
CommandSerializer : defines Command model representation
feilds : ('id', 'date', 'total', 'automobilist','car', 'isVlidated', 'reservation', 'reservationDate', 'reservationAmount')
"""
class CommandSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = models.Command
		fields = ('id', 'date', 'total', 'automobilist','car', 'isValidated', 'reservationAmount')


"""
CommandSerializer : defines Command model representation
feilds : ('id', 'date', 'total', 'automobilist','car', 'isVlidated', 'reservation', 'reservationDate', 'reservationAmount')
"""
class MinCommandSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = models.Command
		fields = ('id')

"""
AutomobilistCommandValidatedNotificationSerializer : defines AutomobilistOfferAcceptNotification model representation
feilds : ('id', 'actor','action_object', 'recepient', 'verb','target')
	actor : manufacturer user
	recipient: command owner
	verb: Manufacturer Name (Marque)
	target = command
"""
class AutomobilistCommandValidatedNotificationSerializer(serializers.ModelSerializer):

	command = serializers.CharField(source='target_object_id') #command id
	commandDate = serializers.ReadOnlyField(source='target.date')
	commandCar = serializers.ReadOnlyField(source='target.car_id')
	commandTotal = serializers.ReadOnlyField(source='target.total')
	manufacturer = serializers.CharField(source='verb')

	class Meta:
		model = models.AutomobilistCommandValidatedNotification
		fields = ('id', 'command', 'recipient', 'manufacturer', 'command', 'commandCar', 'commandTotal','commandDate', 'timestamp', 'unread', 'notification_type')

"""
FollowedVersionSerializer : defines Followed Models  model representation
"""
class FollowedVersionsSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.FollowedVersions
		fields = ('id','version', 'automobilist', 'date')	

"""
FollowedModelsSerializer : defines Followed Models  model representation
"""
class FollowedModelsSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.FollowedModels
		fields = ('id','model', 'automobilist', 'date')	


"""
TransactionSerializer : defines Transaction  model representation
"""
class TransactionSerializer(serializers.ModelSerializer):

	command_car = serializers.ReadOnlyField(source='command.car') 
	automobilist_username = serializers.ReadOnlyField(source='automobilist.username') 
	class Meta:
		model = models.Transaction
		fields = ('id','date', 'state', 'amount', 'automobilist','automobilist_username', 'command', 'command_car')	
		