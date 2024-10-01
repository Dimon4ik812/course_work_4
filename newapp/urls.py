from django.contrib import admin
from django.urls import path
from newapp.apps import NewappConfig


app_name = NewappConfig.name 

urlpatterns = [
    path('',)
]