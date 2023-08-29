from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.db.models import Count
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .serializers import *
from rest_framework.response import Response
from datetime import  timedelta, datetime
# Create your views here.




class accountviewset(ModelViewSet):
    http_method_names=['get','post','patch']

    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user_id=self.request.user.id)
    
    def get_serializer_context(self):
        return {'user_id':self.request.user.id}



    def get_serializer_class(self):
        if self.request.method=='GET':
            return ShowAccountSerializer
        elif self.request.method=='POST':
            return AddAcoountSerializer
        elif self.request.method=='PATCH':
            return UpdateAccountSerializer






class transactions(ModelViewSet):

    http_method_names=['get','post','patch','delete']

    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user__id=self.request.user.id)
    
    def get_serializer_class(self):
        if self.request.method=='GET':
            return ShowTransactionSerializer
        elif self.request.method=='POST':
            return AddTransactionSerializer
        elif self.request.method=='PATCH':
            return UpdateTransaction
        

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}    
























