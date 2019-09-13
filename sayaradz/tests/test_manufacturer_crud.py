import json
from django.contrib.auth.models import User 
from sayaradz import models
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
import http.client

"""
Test methods related to Manufacturer Management
"""
class ManufacturerAPIViewTestCase(APITestCase):

    url = reverse("manufacturers-list")

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="testadmin",email="test@testadmin.com",password="you_know_nothing")
        user.is_superuser = True
        user.is_staff = True
        user.save()

        m = models.Manufacturer.objects.create(name="existing_manifactuerer", nationality="testnationality")
    """
    Test Post new Manifacturer without login
    """  
    def testCreateNewManifacturerWithoutLogin(self):

        response = self.client.post(self.url, {"name": "new_manifactuerer", "nationality": "newnationality"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    """
    Test Post new Manifacturer after login
    """  
    def testCreateNewManufacturer(self):

        #self.client = Client()
        self.client.login(username="testadmin", password="you_know_nothing")

        response = self.client.post(self.url, {"name": "new_manifactuerer", "nationality": "newnationality"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """
    Test Post existing manifacturer name after login
    """  
    def testReCreateExistingManifacturer(self):

        #self.client = Client()
        self.client.login(username="testadmin", password="you_know_nothing")

        response = self.client.post(self.url, {"name": "existing_manifactuerer", "nationality": "newnationality"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Test Get non existing manifacturer name after login
    """  
    def testGetNonFoundManifacturer(self):

        self.client.login(username="testadmin", password="you_know_nothing")

        response = self.client.get("/api/manufacturers/1000/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": "Not found."})

    """
    Test Put new manifacturer name after login
    """  
    def testUpdateManifacturer(self):

        self.client.login(username="testadmin", password="you_know_nothing")
        m = models.Manufacturer.objects.create(name="existing_manifactuerer1", nationality="testnationality1")
        response = self.client.put("/api/manufacturers/"+str(m.id)+"/", {"name":"updated_name", "nationality": "updated_nationality"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"id": m.id,"name": "updated_name", "nationality": "updated_nationality"})

    """
    Test Partial Update existing manufacturer name after login
    """  
    def testPartialUpdateManufacturer(self):

        self.client.login(username="testadmin", password="you_know_nothing")
        m = models.Manufacturer.objects.create(name="existing_manifactuerer2", nationality="testnationality1")
        response = self.client.patch("/api/manufacturers/"+str(m.id)+"/", {"nationality": "updated_nationality"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {"id": m.id,"name": "existing_manifactuerer2", "nationality": "updated_nationality"})

    """
    Test Delete a manufacturer 
    """
    def testDeleteManufacturer(self):

        self.client.login(username="testadmin", password="you_know_nothing")
        m = models.Manufacturer.objects.create(name="existing_manifactuerer2", nationality="testnationality1")
        response = self.client.delete("/api/manufacturers/"+str(m.id)+"/")

        response = self.client.get("/api/manufacturers/"+str(m.id)+"/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {"detail": "Not found."})
