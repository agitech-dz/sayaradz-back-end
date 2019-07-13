from django.db import models
from PIL import Image
import uuid
from django.contrib.auth.models import User 
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from notifications.models import Notification
from model_utils import Choices
from datetime import datetime

#upload ManufacturerUser Avatars from web client to "manufacturerusers_account/avatars/" folder
def get_upload_path1(instance, filename):
        return os.path.join(('images', 'manufacturerusers_avatars' , filename+datetime.now().strftime("%Y/%m/%d")))


#upload Car Photo from mobile client to "cars/photos/" folder
def get_upload_path4(instance, filename):
        return os.path.join(('images', 'automobilists_avatars', filename+datetime.now().strftime("%Y/%m/%d")))

#upload Ad Photo from mobile client to "ads/photos/" folder
def get_upload_path3(instance, filename):
        return '/'.join(['images', 'ads_photos',datetime.now().strftime("%Y/%m/%d")+filename])

#upload Automobilist Avatars from web client to "automobilists_account/avatars/" folder      
def get_upload_path2(instance, filename):
        return os.path.join(['Images', 'cars_photos', filename+datetime.now().strftime("%Y/%m/%d")])

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

    class Meta:
        ordering = ['code']
        unique_together = ("code", "model")

    def __str__(self):
       return self.name


#Color Model [Couleur]
class Color(models.Model):
    code =  models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=50)
    model = models.ForeignKey(MyModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['code']
        unique_together = ("code", "model")
        
    def __str__(self):
       return self.name

#Car Model [Voiture]
class Car(models.Model):

    numChassis = models.CharField(max_length=50, primary_key=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, db_column='color', null=True)
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, db_column='version', null=True)
    options = models.ManyToManyField(Option)
    photo1 = models.ImageField(blank=True, upload_to=get_upload_path2)
    photo2 = models.ImageField(blank=True, upload_to=get_upload_path2)
    photo3 = models.ImageField(blank=True, upload_to=get_upload_path2)
    seller = models.TextField(default="")

    class Meta:
        ordering = ['numChassis']
        
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
    
    dateBegin = models.DateField()
    dateEnd = models.DateField()
    price = models.FloatField()

    class Meta:
        ordering = ['id']

    def __str__(self):
       return self.name

#LigneTarifVersion Model [Ligne Tarif Version] 
class LigneTarifVersion(LigneTarif):
    code = models.OneToOneField(Version, on_delete=models.CASCADE)

    class Meta:
        ordering = ['code']

#LigneTarifOption Model [Ligne Tarif Option]  
class LigneTarifOption(LigneTarif):
    code = models.OneToOneField(Option, on_delete=models.CASCADE)

    class Meta:
        ordering = ['code']

#LigneTarifColor Model [Ligne Tarif Couleur]
class LigneTarifColor(LigneTarif):
    code = models.OneToOneField(Color, on_delete=models.CASCADE)

    class Meta:
        ordering = ['code']

#Automobilist Model [Automobiliste]
class Automobilist(User):
    
    address = models.TextField()
    telephone =  models.CharField(max_length=15)
    avatar = models.ImageField(blank=True, upload_to=get_upload_path4)
    #followedModels = models.ManyToManyField(MyModel)
    #followedVersions = models.ManyToManyField(Version)

    class Meta:
        ordering = ['id']

    def __str__(self):
       return self.username

class FollowedModels(models.Model):

    model = models.ForeignKey(MyModel, on_delete=models.CASCADE)
    automobilist = models.ForeignKey(Automobilist, on_delete = models.CASCADE)
    date = models.DateField(auto_now=True)
    """docstring for FollowedModels"""
   
    class Meta:
        ordering = ['date']

    def __str__(self):
       return self.model + ' ' + self.automobilist

class FollowedVersions(models.Model):

    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    automobilist = models.ForeignKey(Automobilist, on_delete = models.CASCADE)
    date = models.DateField(auto_now=True)
    """docstring for FollowedModels"""
   
    class Meta:
        ordering = ['date']

    def __str__(self):
       return self.version + ' ' + self.automobilist

        

#Command Model [Commande]
class Command(models.Model):

    date = models.DateTimeField(auto_now=True)
    total = models.FloatField()
    automobilist = models.ForeignKey(Automobilist, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    isValidated = models.BooleanField(default=False)
    reservationAmount = models.FloatField(null=True)
    
    class Meta:
        ordering = ['date']
        


#Ad Model [Annonce]
class Ad(models.Model):
    
    model = models.ForeignKey(MyModel, on_delete=models.SET_NULL, null=True)
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)
    photo1 = models.ImageField(blank=True, upload_to=get_upload_path3)
    photo2 = models.ImageField(blank=True, upload_to=get_upload_path3)
    photo3 = models.ImageField(blank=True, upload_to=get_upload_path3)
    minPrice = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    description = models.TextField()
    year = models.CharField(max_length=4)
    distance = models.CharField(max_length=10)
    automobilist = models.ForeignKey(Automobilist, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']
        unique_together = ("id", "automobilist")

#Offer Model [Offre]
class Offer(models.Model):

    date = models.DateTimeField(auto_now=True)
    offredPrice = models.FloatField()
    automobilist = models.ForeignKey(Automobilist, on_delete=models.CASCADE,db_column='automobilist_id')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    isAccepted = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']

#Notify the Automobilist if its offer has been accepted by the Ad owner Notifocation contains  
class AutomobilistNotification(Notification):

    notification_type_choices = Choices(
        ('OA', 'offer_accepted'),#accepter offer
        ('MC', 'model_changed'),
        ('VC', 'version_changed'),
        ('CV', 'command_valitaded'),
    )

    notification_type = models.CharField(max_length=3, choices=notification_type_choices, default=notification_type_choices.OA)

    class Meta:
        ordering = ['timestamp']
        
    
    def __str__(self):
       return self.verb

#Notify the Automobilist if its offer has been accepted by the Ad owner Notifocation contains  
class AutomobilistAcceptOfferNotification(AutomobilistNotification):

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['timestamp']
        
    def __str__(self):
       return self.verb

#Notify the Automobilist if a followed model has been modified  
class AutomobilistFollowedModelChangeNotification(AutomobilistNotification):

    class Meta:
        ordering = ['timestamp']
       
    
    def __str__(self):
       return self.verb

#Notify the Automobilist if a followed version has been modified  
class AutomobilistFollowedVersionChangeNotification(AutomobilistNotification):

    class Meta:
        ordering = ['timestamp']
        
    
    def __str__(self):
       return self.verb

#Notify the Automobilist if a his command has been modified  
class AutomobilistCommandValidatedNotification(AutomobilistNotification):

    class Meta:
        ordering = ['timestamp']
       
    
    def __str__(self):
       return self.verb
