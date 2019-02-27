from django.test import TestCase
from sayaradz.models import Make, MakeUser
from django.contrib.auth.models import User
from django.urls import reverse



from rest_framework.authtoken.models import Token

from rest_framework.test import APITestCase
# Create your tests here.
class  MakeUserTest(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		Make.objects.create(name="MakeTest")
		latestId = Make.objects.latest('id')
		MakeUser.objects.create(email='test@test.com', firstName='testfirstName', familyName='testfamilyName', password='000', address='testaddress', telephone='testtelephone', make=latestId)


	def testMakeContent(self):
		make = Make.objects.latest('id')
		expectedMakeName = f'{make.name}'
		self.assertEquals(expectedMakeName, 'MakeTest')

	def testMakeUserContent(self):
		makeUser = MakeUser.objects.latest('id')
		expectedMakeUserMail = f'{makeUser.email}'
		self.assertEquals(expectedMakeUserMail, 'test@test.com')



