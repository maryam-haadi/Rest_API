from collections.abc import Iterable
from django.db import models
# from django.contrib.auth.models import User
from uuid import uuid4
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.





class User(AbstractUser):
    
  phone=models.CharField(max_length=255,    validators=[
      RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format '+123456789'. Up to 15 digits allowed."
      ),
  ],default='+98')



    
class Account(models.Model):

    id=models.UUIDField(primary_key=True,default=uuid4)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    balance=models.DecimalField(max_digits=20,decimal_places=2,default=0)  



    def __str__(self):
        return str(self.id)




    

class Transaction(models.Model):
    id=models.IntegerField(primary_key=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    transaction_value=models.DecimalField(max_digits=20, decimal_places=2)
    description=models.CharField(max_length=500)
    recorde_date=models.DateTimeField(auto_now_add=True)
    account=models.ForeignKey(Account,on_delete=models.CASCADE)    


    def __str__(self):
        return self.user.username
    
















