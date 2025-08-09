from django.contrib.auth.models import UserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import datetime

from .managers import CustomUserManager

# Create your models here.
USER_PROFILE_CHOICES = {
    'REGULAR':'Regular',
    'MODO':'Moderator',
    'ADMIN':'Admin'
}

GENDER_CHOICES = {
    'M':'Masculin',
    'F':'Feminin',
    'O':'Autre'
}


               
class User(AbstractUser):
    email = models.EmailField(_("Adresse email"), max_length=254, unique=True)
    first_name = models.CharField(_("Prénom"), max_length=50)
    last_name = models.CharField(_("Nom"), max_length=50)
    birthdate = models.DateField(_("Date de naissance"), auto_now=False, auto_now_add=False)
    gender = models.CharField(_("Genre"), choices=GENDER_CHOICES)
    #profile_pic = models.ImageField(_("Photo de profile"), upload_to="images/profile_pictures", height_field=None, width_field=None, max_length=None)
    profile = models.CharField(choices=USER_PROFILE_CHOICES, default='REGULAR')

    is_verified = models.BooleanField(_("Compte vérifié"), default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(_("Mise à jour"), auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthdate', 'gender', 'profile']


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return f"{self.first_name} + {" "} + {self.last_name}"
    
    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]

    def __str__(self):
        return self.first_name

    def is_eligible(self):
        return timezone.now() - self.birthdate >= datetime.timedelta(days=5840)




