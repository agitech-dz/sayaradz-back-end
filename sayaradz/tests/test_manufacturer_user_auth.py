import json
from django.contrib.auth.models import User 
from sayaradz import models
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
import http.client

"""
Test methods related ro manifacturer user registration
"""
class ManufacturerUserRegistrationAPIViewTestCase(APITestCase):

	url = reverse("register_manufactureruser")

	@classmethod
	def setUpTestData(cls):

		models.Manufacturer.objects.create(name="testmanufacturer", nationality="testnationality")
		cls.manufacturerID = models.Manufacturer.objects.order_by('-id')[0]

	"""
	Test post call with invalid passwords
	"""
	def testInvalidPassword(self):

		manufacturerUserData = {
			"username": "testuser",
			"email": "test@testuser.com",
			"password": "password",
			"confirm_password": "INVALID_PASSWORD",
			"address": "testaddress",
			"manufacturer": self.manufacturerID.id,
			"telephone": "00000"
		}

		response = self.client.post(self.url,manufacturerUserData)
		#Register Fails
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	"""
	Test a post call with user valid data
	"""
	def testManifacturerUserRegistration(self):

		manufacturerUserData = {
			"username": "testuser88",
			"email": "test@testuser.com",
			"password": "123123",
			"confirm_password": "123123",
			"address":"testaddress",
			"manufacturer": self.manufacturerID.id,
			"telephone": "00000"
		}

		response = self.client.post(self.url, manufacturerUserData, format='json')

		#Validate manufacturer user registration [Creation]
		print(response)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(models.ManufacturerUser.objects.count(), 1)
		self.assertEqual(models.ManufacturerUser.objects.get().username, 'testuser88')

		#Validate auth_token generation
		self.assertTrue("token" in json.loads(response.content))

	"""
	Test a post call with already exists username
	"""
	def testUniqueUsernameValidation(self):

		manifacturerUserData1 = {
			"username": "testuser1",
			"email": "test1@testuser.com",
			"password": "123123",
			"confirm_password": "123123",
			"address":"testaddress",
			"manufacturer": self.manufacturerID.id,
			"telephone": "00000"
		}

		response = self.client.post(self.url, manifacturerUserData1, format='json')

		#Validate manifacturer user registration [Creation]
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		manifacturerUserData2 = {
			"username": "testuser1",
			"email": "test2@testuser.com",
			"password": "DOES_NOT_EXIST",
			"confirm_password": "DOES_NOT_EXIST",
			"address":"testaddress",
			"manufacturer": self.manufacturerID.id,
			"telephone": "00000"
		}

		response = self.client.post(self.url, manifacturerUserData2, format='json')
		#Manufacturer user registration fails
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
