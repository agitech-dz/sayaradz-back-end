
from django.db import models
from PIL import Image
import uuid

from django.contrib.auth.models import User

# Create your models here.
def get_upload_path1(instance, filename):
        return os.path.join('makeusers_account/avatars/', now().date().strftime("%Y/%m/%d"), filename)

def get_upload_path2(instance, filename):
        return os.path.join('cars/photos/', now().date().strftime("%Y/%m/%d"), filename)

def get_upload_path3(instance, filename):
        return os.path.join('ads/photos/', now().date().strftime("%Y/%m/%d"), filename)
        
def get_upload_path4(instance, filename):
        return os.path.join('automobilists_account/avatars/', now().date().strftime("%Y/%m/%d"), filename)



#Utilisateur Fabricant

class MakeUser(models.Model):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    firstName = models.CharField(max_length=50)
    familyName = models.CharField(max_length=50)
    password = models.CharField(max_length=100, default='')
    address = models.TextField()
    telephone =  models.CharField(max_length=15)
    isBlocked = models.BooleanField(default=False)
    make = models.ForeignKey( 'Make', on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to=get_upload_path1)


    


    def save(self, *args, **kwargs):
        super(MakeUser, self).save(*args, **kwargs) # Call the real   save() method


#Fabricant
class Make(models.Model):

    name = models.CharField(max_length=75, unique=True)
    #natinality = models.CharField(max_length=45)
    def __str__(self):
       return self.name

class Model(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)

    def __str__(self):
       return self.name

class Version(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
       return self.name

#Concessionnaire
class CarSeller(models.Model):
    name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15)

    def __str__(self):
       return self.name

#Option
class Option(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    versions = models.ManyToManyField(Version)

    def __str__(self):
       return self.name

class Color(models.Model):
    code =  models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)

    def __str__(self):
       return self.name

#Véhicule
class Car(models.Model):
    numChassis = models.CharField(max_length=50, primary_key=True)
    color = models.ForeignKey(Model, on_delete=models.SET_NULL, db_column='color', null=True)
    version = models.ForeignKey(Make, on_delete=models.SET_NULL, db_column='version', null=True)
    options = models.ManyToManyField(Option)
    photo1 = models.ImageField(blank=True, upload_to=get_upload_path2)
    photo2 = models.ImageField(blank=True, upload_to=get_upload_path2)
    photo3 = models.ImageField(blank=True, upload_to=get_upload_path2)
    seller = models.ForeignKey(CarSeller, on_delete=models.SET_NULL, null=True)

    

#Véhicule Occasion
class OccCar(Car):

    def __str__(self):
       return self.numChassis

#Véhicule nouvel
class NewCar(Car):

    def __str__(self):
       return self.numChassis



class LigneTarif(models.Model):
    
    dataBegin = models.DateField()
    dataEnd = models.DateField()
    price = models.FloatField()

    def __str__(self):
       return self.name

class LigneTarifVersion(LigneTarif):
    code = models.OneToOneField(Version, on_delete=models.CASCADE)
     
class LigneTarifOption(LigneTarif):
    code = models.OneToOneField(Option, on_delete=models.CASCADE)

class LigneTarifColor(LigneTarif):
    code = models.OneToOneField(Color, on_delete=models.CASCADE)


class Automobilist(models.Model):
    #email = models.EmailField(max_length=255, unique=True, db_index=True)
    firstName = models.CharField(max_length=50)
    familyName = models.CharField(max_length=50)
    password = models.CharField(max_length=100, default='')
    address = models.TextField()
    telephone =  models.CharField(max_length=15)
    avatar = models.ImageField(blank=True, upload_to=get_upload_path4)
    followedModels = models.ManyToManyField(Model)
    followedVersions = models.ManyToManyField(Version)


    
    def __str__(self):
       return self.name


class Command(models.Model):
    date = models.DateField()
    price = models.FloatField()
    automobilist = models.ForeignKey(Automobilist, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    isVlidated = models.BooleanField(default=False)


    def __str__(self):
       return self.name

#Annonce
class Ad(models.Model):
    minPrice = models.FloatField()
    date = models.DateField()
    automobilist = models.ForeignKey(Automobilist, on_delete=models.CASCADE, db_column='owner_id')
    car = models.OneToOneField(OccCar, on_delete=models.CASCADE, db_column='car_numChassis')
    photo1 = models.ImageField(blank=True, upload_to=get_upload_path3)
    photo2 = models.ImageField(blank=True, upload_to=get_upload_path3)
    photo3 = models.ImageField(blank=True, upload_to=get_upload_path3)
    
    
#Offre
class Offer(models.Model):
    date = models.DateField()
    offredAmount = models.FloatField()
    automobilist = models.ForeignKey(Automobilist, on_delete=models.CASCADE,db_column='automobilist_id')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    isAccepted = models.BooleanField(default=False)
    