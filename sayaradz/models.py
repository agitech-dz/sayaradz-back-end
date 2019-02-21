
from django.db import models

import uuid

from django.contrib.auth.models import User

# Create your models here.

#Utilisateur Fabricant

class MakeUser(models.Model):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    firstName= models.CharField(max_length=50)
    familyName = models.CharField(max_length=50)
    password = models.CharField(max_length=100, default='')
    address = models.TextField()
    telephone =  models.CharField(max_length=15)
    isBlocked = models.BooleanField(default=False)
    make = models.ForeignKey( 'Make', on_delete=models.CASCADE)



    def save(self, *args, **kwargs):
        super(MakeUser, self).save(*args, **kwargs) # Call the real   save() method


#Fabricant
class Make(models.Model):

    name = models.CharField(max_length=75, unique=True)
    #natinality = models.CharField(max_length=45)
    def __str__(self):
       return self.name