from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *



class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields=['id','username','password','email']
    
    
    def create(self,validated_data):
        user = User.objects.create(is_active=True,**validated_data)
        user.is_active=True
        user.save()
        return user

        

class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields=['id','username','email']





class ShowAccountSerializer(serializers.ModelSerializer):

    deposits=serializers.SerializerMethodField(method_name='total_deposits',read_only=True)
    expenses=serializers.SerializerMethodField(method_name='total_expenses',read_only=True)

    class Meta:
        model=Account
        fields=['id','user','first_name','last_name','balance','phone','deposits','expenses']

    def total_deposits(self,account:Account):
        total=0
        accounts=Account.objects.filter(user_id=self.context['user_id'])
        for acount in accounts:
            total+=acount.balance
        return total   

    def total_expenses(self,account:Account):
        total=0
        transactions=Transaction.objects.filter(user_id=self.context['user_id'],account=account)

        for transaction in transactions:
            if transaction.transaction_value < 0 :
                total -=transaction.transaction_value

        return total

    

class AddAcoountSerializer(serializers.ModelSerializer):

    class Meta:
        model=Account
        fields=['first_name','last_name','phone','balance']

    def create(self, validated_data):
        account=Account.objects.create(user_id=self.context['user_id'], **validated_data)
        return account    


class UpdateAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model=Account
        fields=['first_name','last_name','phone','balance']

        

class ShowTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model=Transaction
        fields='__all__'

class AddTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model=Transaction
        fields=['transaction_value','description','account']


    def validate(self, attrs):
        if attrs['account'] not in Account.objects.filter(user=self.context['user_id']):
            raise serializers.ValidationError("this account is not for you!")
        
        if attrs['account'].balance + attrs['transaction_value'] < 0:
            raise serializers.ValidationError("insufficient inventory!")
        
        return attrs

    def create(self, validated_data):
        user=User.objects.get(id=self.context['user_id'])
        transaction=Transaction.objects.create(user=user,**validated_data)
        account=validated_data['account']
        trans_value=validated_data['transaction_value']
        account.balance+=trans_value
        account.save()
        return transaction



class UpdateTransaction(serializers.ModelSerializer):

    class Meta:
        model=Transaction
        fields=['transaction_value','description','account']

    def save(self,validated_data):

        user=User.objects.get(id=self.context['user_id'])
        transaction=Transaction.objects.create(user=user,**validated_data)
        account=validated_data['account']
        trans_value=validated_data['transaction_value']
        account.balance+=trans_value
        account.save()
        return transaction






