from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.core.validators import RegexValidator
# Create your models here.


class Account(models.Model):

    id=models.UUIDField(primary_key=True,default=uuid4)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255,default='-')
    last_name=models.CharField(max_length=255,default='-')
    phone=models.CharField(max_length=255,    validators=[
      RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format '+123456789'. Up to 15 digits allowed."
      ),
    ],default='+98')
    balance=models.DecimalField(max_digits=20,decimal_places=2,default=0)  ##



    def __str__(self):
        return str(self.id)



# # class Customer(models.Model):

# #     user=models.ForeignKey(User,on_delete=models.CASCADE)
# #     account=models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)


#     def __str__(self):
#         return self.user.username
    

class Transaction(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    # transaction_value=models.IntegerField()
    transaction_value=models.DecimalField(max_digits=20, decimal_places=2)
    description=models.CharField(max_length=500)
    recorde_date=models.DateTimeField(auto_now_add=True)
    account=models.ForeignKey(Account,on_delete=models.CASCADE)##    


    def __str__(self):
        return self.user.username
    
















