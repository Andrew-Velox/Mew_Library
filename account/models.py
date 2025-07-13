from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE
# Create your models here.


class UserLibraryAccount(models.Model):
    user = models.OneToOneField(User,related_name='account' , on_delete=models.CASCADE)
    gender = models.CharField(max_length=10,choices=GENDER_TYPE)
    balance = models.DecimalField(default=0,max_digits=12,decimal_places=2)
    initial_borrow_date = models.DateField(auto_now=True)
    birth_date = models.DateField(null=True,blank=True)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return str(self.user.username)