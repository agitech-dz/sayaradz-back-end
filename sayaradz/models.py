
from django.db import models
from PIL import Image
import uuid
from django.contrib.auth.models import User 
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token


#upload ManufacturerUser Avatars from web client to "manufacturerusers_account/avatars/" folder
def get_upload_path1(instance, filename):
        return os.path.join('manufacturerusers_account/avatars/', now().date().strftime("%Y/%m/%d"), filename)


#upload Car Photo from mobile client to "cars/photos/" folder
def get_upload_path2(instance, filename):
        return os.path.join('cars/photos/', now().date().strftime("%Y/%m/%d"), filename)

#upload Ad Photo from mobile client to "ads/photos/" folder
def get_upload_path3(instance, filename):
        return os.path.join('ads/photos/', now().date().strftime("%Y/%m/%d"), filename)

#upload Automobilist Avatars from web client to "automobilists_account/avatars/" folder      
def get_upload_path4(instance, filename):
        return os.path.join('automobilists_account/avatars/', now().date().strftime("%Y/%m/%d"), filename)

#ManufacturerUser Model [Utilisateur Fabricant]
class ManufacturerUser(User):
   
    address = models.TextField()
    telephone =  models.CharField(max_length=15)
    manufacturer = models.ForeignKey( 'manufacturer', on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to=get_upload_path1)
    is_blocked = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        super(ManufacturerUser, self).save(*args, **kwargs) # Call the real   save() method

#Manufacturer Model [Fabricant]
class Manufacturer(models.Model):
    name = models.CharField(max_length=75, unique=True)
    nationality = models.CharField(max_length=45, blank=True)

    class Meta:
        ordering = ['id']
        
    def __str__(self):
       return self.name

#Model Model [Modèle]
class MyModel(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    class Meta:
        ordering = ['code']
        unique_together = ("code", "manufacturer")

    def __str__(self):
       return self.name

#Option Model [Option]
class Option(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    model = models.ForeignKey(MyModel, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['code']
        unique_together = ("code", "model")

    def __str__(self):
       return self.name
       
#Version Model [Version]
class Version(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    options = models.ManyToManyField(Option)
    model = models.ForeignKey(MyModel, on_delete=models.CASCADE)

    def __str__(self):
       return self.name


#CarSeller Model [Concessionnaire]
class CarSeller(models.Model):
    name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15)

    def __str__(self):
       return self.name

#Color Model [Couleur]
class Color(models.Model):
    code =  models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)
    model = models.ForeignKey(MyModel, on_delete=models.CASCADE)

    def __str__(self):
       return self.name

#Car Model [Voiture]
class Car(models.Model):
    numChassis = models.CharField(max_length=50, primary_key=True)
    color = models.ForeignKey(MyModel, on_delete=models.SET_NULL, db_column='color', null=True)
    version = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, db_column='version', null=True)
    options = models.ManyToManyField(Option)
    photo1 = models.ImageField(blank=True, upload_to=get_upload_path2)
    photo2 = models.ImageField(blank=True, upload_to=get_upload_path2)
    photo3 = models.ImageField(blank=True, upload_to=get_upload_path2)
    seller = models.ForeignKey(CarSeller, on_delete=models.SET_NULL, null=True)

#OccCar Model [Voiture Occasion] 
class OccCar(Car):

    def __str__(self):
       return self.numChassis

#NewCar Model [Voiture Neuve] 
class NewCar(Car):

    def __str__(self):
       return self.numChassis

#LigneTarif Model [Ligne Tarif] 
class LigneTarif(models.Model):
    
    dataBegin = models.DateField(auto_now=True)
    dataEnd = models.DateField(auto_now=True)
    price = models.FloatField()

    def __str__(self):
       return self.name

#LigneTarifVersion Model [Ligne Tarif Version] 
class LigneTarifVersion(LigneTarif):
    code = models.OneToOneField(Version, on_delete=models.CASCADE)

#LigneTarifOption Model [Ligne Tarif Option]  
class LigneTarifOption(LigneTarif):
    code = models.OneToOneField(Option, on_delete=models.CASCADE)

#LigneTarifColor Model [Ligne Tarif Couleur]
class LigneTarifColor(LigneTarif):
    code = models.OneToOneField(Color, on_delete=models.CASCADE)

#Automobilist Model [Automobiliste]
class Automobilist(models.Model):
    #email = models.EmailField(max_length=255, unique=True, db_index=True)
    firstName = models.CharField(max_length=50)
    familyName = models.CharField(max_length=50)
    password = models.CharField(max_length=100, default='')
    address = models.TextField()
    telephone =  models.CharField(max_length=15)
    avatar = models.ImageField(blank=True, upload_to=get_upload_path4)
    followedModels = models.ManyToManyField(MyModel)
    followedVersions = models.ManyToManyField(Version)

    def __str__(self):
       return self.name

#Command Model [Commande]
class Command(models.Model):
    date = models.DateTimeField(auto_now=True)
    price = models.FloatField()
    automobilist = models.ForeignKey(Automobilist, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    isVlidated = models.BooleanField(default=False)


    def __str__(self):
       return self.name

#Ad Model [Annonce]
class Ad(models.Model):
    minPrice = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    automobilist = models.ForeignKey(Automobilist, on_delete=models.CASCADE, db_column='owner_id')
    car = models.OneToOneField(OccCar, on_delete=models.CASCADE, db_column='car_numChassis')
    photo1 = models.ImageField(blank=True, upload_to=get_upload_path3)
    photo2 = models.ImageField(blank=True, upload_to=get_upload_path3)
    photo3 = models.ImageField(blank=True, upload_to=get_upload_path3)

#Offer Model [Offre]
class Offer(models.Model):
    date = models.DateTimeField(auto_now=True)
    offredAmount = models.FloatField()
    automobilist = models.ForeignKey(Automobilist, on_delete=models.CASCADE,db_column='automobilist_id')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    isAccepted = models.BooleanField(default=False)
    




