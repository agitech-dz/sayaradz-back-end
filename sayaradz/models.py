
from django.db import models
from PIL import Image
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager 
from django.utils.translation import ugettext_lazy as _



# Create your models here.
def get_upload_path1(instance, filename):
        return os.path.join('makeusers_account/avatars/', now().date().strftime("%Y/%m/%d"), filename)

def get_upload_path2(instance, filename):
        return os.path.join('cars/photos/', now().date().strftime("%Y/%m/%d"), filename)

def get_upload_path3(instance, filename):
        return os.path.join('ads/photos/', now().date().strftime("%Y/%m/%d"), filename)
        
def get_upload_path4(instance, filename):
        return os.path.join('automobilists_account/avatars/', now().date().strftime("%Y/%m/%d"), filename)

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

#My User (change defaut UserAuth form username to mail )
class MyUser(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


#Utilisateur Fabricant

class MakeUser(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, default=1)
    address = models.TextField()
    telephone =  models.CharField(max_length=15)
    make = models.ForeignKey( 'Make', on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to=get_upload_path1)
    
    def save(self, *args, **kwargs):
        super(MakeUser, self).save(*args, **kwargs) # Call the real   save() method

#Fabricant
class Make(models.Model):

    name = models.CharField(max_length=75, unique=True)
    nationality = models.CharField(max_length=45, blank=True)
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
    
    dataBegin = models.DateField(auto_now=True)
    dataEnd = models.DateField(auto_now=True)
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
    date = models.DateTimeField(auto_now=True)
    price = models.FloatField()
    automobilist = models.ForeignKey(Automobilist, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    isVlidated = models.BooleanField(default=False)


    def __str__(self):
       return self.name

#Annonce
class Ad(models.Model):
    minPrice = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    automobilist = models.ForeignKey(Automobilist, on_delete=models.CASCADE, db_column='owner_id')
    car = models.OneToOneField(OccCar, on_delete=models.CASCADE, db_column='car_numChassis')
    photo1 = models.ImageField(blank=True, upload_to=get_upload_path3)
    photo2 = models.ImageField(blank=True, upload_to=get_upload_path3)
    photo3 = models.ImageField(blank=True, upload_to=get_upload_path3)
    
    
#Offre
class Offer(models.Model):
    date = models.DateTimeField(auto_now=True)
    offredAmount = models.FloatField()
    automobilist = models.ForeignKey(Automobilist, on_delete=models.CASCADE,db_column='automobilist_id')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    isAccepted = models.BooleanField(default=False)
    




# SIGNALS AND LISTENERS
from django.db.models.signals import post_save
from django.dispatch import receiver


# this snippet makes the ORM create a (MakeUser) profile each time an user is created (or updated, if the user profile lost), including 'admin' user.
@receiver(post_save, sender=MyUser)
def create_makeuser(sender, instance, created, **kwargs):
    if created:
        if not MyUser.is_superuser:
            MakeUser.objects.create(user=instance)

@receiver(post_save, sender=MyUser)
def save_makeuser(sender, instance, **kwargs):
    instance.MakeUser.save()