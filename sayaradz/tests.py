from django.test import TestCase
from sayaradz.models import Make, MakeUser
# Create your tests here.
class  MakeUserTest(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		Make.objects.create(name="MakeTest")
		latestId = Make.objects.latest('id')
		MakeUser.objects.create(email='test@test.com', firstName='testfirstName', familyName='testfamilyName', password='000', address='testaddress', telephone='testtelephone', make=latestId)


	def testMakeContent(self):
		make = Make.objects.latest('id')
		expectedMakeName = make.name
		self.assertEquals(expectedMakeName, 'MakeTest')

	def testMakeUserContent(self):
		makeUser = MakeUser.objects.latest('id')
		expectedMakeUserMail = makeUser.email
		self.assertEquals(expectedMakeUserMail, 'test@test.com')



