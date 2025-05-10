from django.contrib import admin
from django.urls import path
from . import views  # Import your app's views
from django.contrib.auth import views as auth
from django.contrib.auth import views as auth_views
urlpatterns = [
 path('', views.farming, name='farming'),
 path('crop/',views.crop,name='crop'),]