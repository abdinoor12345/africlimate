from django import forms
from .models import Doctor
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Croping,ProductData,AgriculturalPost,Inquiry
class DoctorForm(forms.ModelForm):
    
    class Meta:   
        model = Doctor
        fields = ['name', 'email', 'phone', 'specialty', 'department', 'research_area', 'publications_count', 'date_joined', 'active']


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    phone_no = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_no', 'password1', 'password2']
class WeatherForm(forms.Form): 
         city = forms.CharField(max_length=100, label='Enter a city')
class CroppingForm(forms.ModelForm):
    
      class Meta:
             model=Croping
             
             fields = ['name', 'optimal_temperature_min', 'optimal_temperature_max', 'optimal_humidity_min', 'optimal_humidity_max', 'optimal_soil_moisture_min', 'optimal_soil_moisture_max'
                       ,'image_url','description']
class ProductForm(forms.ModelForm):
      class Meta:
          model=ProductData
          fields=['product_name','product_type','image_url','warranty_period','price','seed_type','growth_duration',
                  'available_quantity','description','location',]
          
class BlogForm(forms.ModelForm):
      class Meta:
          model=AgriculturalPost
          fields=['title','content','image_url']
          
class Inquiry(forms.ModelForm):
      class Meta:
          model=Inquiry
          fields=['name','email','phone','message']
CROP_CHOICES = [
    ('maize', 'Maize'),
    ('rice', 'Rice'),
    ('beans', 'Beans'),
    ('tomato', 'Tomato'),
    ('wheat', 'Wheat'),
    ('sorghum', 'Sorghum'),
    ('cassava', 'Cassava'),
    ('potato', 'Potato'),
    ('soybean', 'Soybean'),
    ('cotton', 'Cotton'),
    ('barley', 'Barley'),
    ('millet', 'Millet'),
    ('sugarcane', 'Sugarcane'),
    ('coffee', 'Coffee'),
    ('tea', 'Tea'),
]
class LocationForm(forms.Form):
    location = forms.CharField(label="Enter a location", max_length=100)
    crop = forms.ChoiceField(label="Select crop", choices=CROP_CHOICES)
          