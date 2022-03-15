from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from django.db.models.signals import pre_save , post_save
from account.slug_generator import unique_slug_generator
# from datetime import datetime
from django.utils.timezone import now



# from django.contrib.auth import get_user_model
# User = get_user_model()


TAGS = (('React','React'),('Python','Python'),('Tech','Tech'),('Java','Java'))
PROF = (('Doctor','Doctor'),('Developer','Developer'),('Hr','Hr'),('Manager','Manager'))


class UserManager(BaseUserManager):

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)



    def create_superuser(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')    
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class DoctorManager(models.Manager):
    def get_doctors(self):
        return self.filter(proffession='Doctor')

class DeveloperManager(models.Manager):
    def get_developer(self):
        return self.filter(proffession='Developer')

class HrManager(models.Manager):
    def get_hr(self):
        return self.filter(proffession='Hr')





class User(AbstractUser, models.Model):
    company = models.CharField(max_length = 20, blank = True, null= True,default='Hello')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(default=now,blank=True,null= True)
    tags = models.CharField(choices = TAGS,max_length = 100,default = 'Tech')
    slug = models.SlugField(max_length=100,blank=True,null=True)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

def slug_generator(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator,sender=User)

def create_userdetails(sender,instance,*args,**kwargs):
    UserDetails.objects.create(user=instance)

post_save.connect(create_userdetails,sender=User)

class Common(models.Model):
    register_as = models.CharField(max_length=20, blank = True,null= True)
    class Meta:
        abstract = True

class UserDetails(Common):
    user = models.OneToOneField(User, on_delete = models.CASCADE,blank=True, null=True)
    profile_image = models.ImageField(upload_to ='image/',default='image/Screenshot_from_2022-01-19_15-11-15.png')
    proffession = models.CharField(choices = PROF,max_length = 50,default = 'Doctor')
    objects = models.Manager()
    doctors = DoctorManager()
    developer = DeveloperManager()
    hrs = HrManager()

    def __str__(self):
        return self.user.email





