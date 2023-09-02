from django.urls import path,include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from pprint import pprint
from .views import *


router=DefaultRouter()
router.register('transactions',transactions,basename='transactions')
router.register('account',accountviewset,basename='account')







urlpatterns=[

    path('',include(router.urls))
    
]






























