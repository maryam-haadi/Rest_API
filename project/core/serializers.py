from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *




class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields=['id','username','password','email','first_name','last_name','phone']
    
    
    def create(self,validated_data):
        user = User.objects.create(**validated_data)
        # user=super().create(validated_data)
        user.set_password(validated_data['password'])
        user.is_active=True
        user.save()
        account=Account.objects.create(user=user)
        return user

        

class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields=['id','username','email','phone']





class ShowAccountSerializer(serializers.ModelSerializer):

    deposits=serializers.SerializerMethodField(method_name='total_deposits',read_only=True)
    expenses=serializers.SerializerMethodField(method_name='total_expenses',read_only=True)

    class Meta:
        model=Account
        fields=['id','user','balance','deposits','expenses']

    def total_deposits(self,account:Account):
        total=0


        transactions=Transaction.objects.filter(user_id=self.context['user_id'],account=account)
        for transaction in transactions:
            if transaction.transaction_value > 0 :
                total +=transaction.transaction_value
        return total   

    def total_expenses(self,account:Account):
        total=0
        transactions=Transaction.objects.filter(user_id=self.context['user_id'],account=account)

        for transaction in transactions:
            if transaction.transaction_value < 0 :
                total -=transaction.transaction_value

        return total

    







class ShowTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model=Transaction
        fields='__all__'




class AddTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model=Transaction
        fields=['transaction_value','description']


    def validate(self, attrs):
        user=User.objects.get(id=self.context['user_id'])
        account=Account.objects.filter(user=user).first()
        if account is None:
            account=Account.objects.create(user=user)

        if account.balance + attrs['transaction_value'] < 0:
            raise serializers.ValidationError("insufficient inventory!")
        
        return attrs

    def create(self, validated_data):
        user=User.objects.get(id=self.context['user_id'])
        account=Account.objects.filter(user=user).first()
        if account is None:
            account=Account.objects.create(user=user)

        transaction=Transaction.objects.create(user=user,**validated_data,account=account)
        trans_value=validated_data['transaction_value']
        account.balance+=trans_value
        account.save()
        return transaction




class UpdateTransaction(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields=['id','transaction_value','description']



    def validate(self,attrs):
       
        instance=Transaction.objects.filter(id=attrs['id']).first()
        if instance is None:
             raise serializers.ValidationError("you can not this update!")


        old_transaction_value=instance.transaction_value
        new_transaction_value=attrs['transaction_value']

        account=Account.objects.filter(user=self.context['user_id']).first()

        value=old_transaction_value - new_transaction_value
        amount=account.balance - value
        if amount < 0:
            raise serializers.ValidationError("you can not this update! because your balance is not enough")

        return attrs

            



    def update(self, instance, validated_data):
        old_transaction_value=instance.transaction_value
        new_transaction_value=validated_data['transaction_value']

        account=Account.objects.filter(user=self.context['user_id']).first()

        value=old_transaction_value - new_transaction_value
        account.balance -=value
        account.save()

        instance.transaction_value=new_transaction_value
        instance.description=validated_data['description']
        

        instance.save()
        return instance
    
    






