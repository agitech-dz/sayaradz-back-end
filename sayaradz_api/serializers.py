from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from sayaradz.models import Make, MakeUser, MyUser

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'password' , 'is_superuser')


# Serializers define the API representation.
class MakeSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Make
		fields = ('id','name', 'nationality')


# Serializers define the API representation.
class MakeUserSerializer(serializers.ModelSerializer):
	user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	class Meta:
		model = MakeUser
		fields = ('address', 'telephone', 'make', 'user')


class AdminLoginSerializer(serializers.Serializer):

	email = serializers.EmailField(required=True)
	password = serializers.CharField(required=True)

	default_error_messages = {
		'inactive_account': _('User account is disabled.'),
		'invalid_credentials': _('Unable to login with provided credentials.')
	}

	def __init__(self, *args, **kwargs):

		super(AdminLoginSerializer, self).__init__(*args, **kwargs)
		self.user = None


	def validate(self, attrs):
		self.user = authenticate(email=attrs.get("email"), password=attrs.get('password'))
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
		fields = ("auth_token", "created")

class MakeUserLoginSerializer(serializers.Serializer):

	email = serializers.CharField(required=True)
	password = serializers.CharField(required=True)

	default_error_messages = {
		'inactive_account': _('User account is disabled.'),
		'invalid_credentials': _('Unable to login with provided credentials.')
	}

	def __init__(self, *args, **kwargs):
		super(MakeUserLoginSerializer, self).__init__(*args, **kwargs)
		self.user = None

	def validate(self, attrs):

		self.user = authenticate(email=attrs.get("email"), password=attrs.get('password'))
		if self.user:

			if not self.user.is_active:
				raise serializers.ValidationError(self.error_messages['inactive_account'])

			return attrs

		else:
			raise serializers.ValidationError(self.error_messages['invalid_credentials'])
