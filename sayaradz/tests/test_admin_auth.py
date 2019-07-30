import json
from django.contrib.auth.models import User 
from sayaradz import models
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
import http.client

"""
Test methods related to admin registration
"""
class AdminRegistrationAPIViewTestCase(APITestCase):
	
	url = reverse("register_admin")
	"""
	Test post call with invalid passwords
	"""	
	def testInvalidPassword(self):

		adminData = {
			"first_name": "test_admin",
			"last_name": "test_admin",
			"username": "testadmin",
			"email": "test@testadmin.com",
			"password": "654654",
			"confirm_password": "INVALID_PASSWORD"
		}

		response = self.client.post(self.url,adminData)
		#Register Fails
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	"""
	Test a post call with user valid data
	"""
	def testAdminRegistration(self):

		adminData = {
			"first_name": "test_admin",
			"last_name": "test_admin",
			"username": "testadmin",
			"email": "test@testadmin.com",
			"password": "654654",
			"confirm_password": "654654"
		}

		response = self.client.post(self.url, adminData, format='json')

		#Validate admin registration [Creation]
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(User.objects.get().username, 'testadmin')

		#Validate auth_token generation
		self.assertTrue("token" in json.loads(response.content))

	"""
	Test a post call with already exists username
	"""
	def testUniqueUsernameValidation(self):

		adminData1 = {
			"username": "testadmin1",
			"email": "test1@testadmin.com",
			"password": "123123",
			"confirm_password": "123123"
		}

		response = self.client.post(self.url, adminData1, format='json')

		#Validate Admin registration [Creation]
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		adminData2 = {
			"username": "testadmin1",
			"email": "test2@testadmin.com",
			"password": "DOES_NOT_EXIST",
			"confirm_password": "DOES_NOT_EXIST"
		}

		response = self.client.post(self.url, adminData2, format='json')
		#Admin registration fails
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


"""
Test methods related to Admin Authentification [Login]
"""
class AdminLoginAPIViewTestCase(APITestCase):

	url = reverse("login__")
	"""
	Regiter new admin
	"""
	@classmethod
	def setUpTestData(cls):
		user = User.objects.create_user(username="testadmin",email="test@testadmin.com",password="you_know_nothing")
		user.is_superuser = True
		user.is_staff = True
		user.save()

	"""
	Test Login without sending password in the post call
	"""
	def testAdminAuthenticationWithoutPassword(self):

		response = self.client.post(self.url, {"username": "testadmin"})

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	"""
	Test Login with wrong password
	"""
	def testAuthenticationWithWrongPassword(self):

		response = self.client.post(self.url, {"username": "testadmin", "password": "I_know"})

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	"""
	Test Login with valid data
	"""
	def testAuthenticationWithValidData(self):

		response = self.client.post(self.url, {"username": "testadmin", "password": "you_know_nothing"}, format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.assertTrue("auth_token" in json.loads(response.content))

