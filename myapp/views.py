from django.shortcuts import render, redirect,get_object_or_404, HttpResponseRedirect
from .models import Doctor ,Croping,ProductData,AgriculturalPost
# from .models import SatelliteImage
from .forms import DoctorForm,CroppingForm,ProductForm,BlogForm,Inquiry
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib import messages

from django.shortcuts import get_object_or_404
from .models import Profile
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.http import JsonResponse
import openai
import os
from .models import Chat
from .models import Croping
from django.utils import timezone
import os
import requests
from django.conf import settings
from .forms import WeatherForm
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import LocationForm
from .pestcheck.utils import get_coordinates, get_pest_forecast
def get_weather_data(city):
    api_key = '7e06f63d943f3bda76f5a47e9ebd3403'  # Replace with your OpenWeatherMap API key
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}
    response = requests.get(base_url, params=params)
    return response.json()
 
 
def recommend_crops(temperature, humidity, soil_moisture):
    crops = Croping.objects.filter(
        optimal_temperature_min__lte=temperature,
        optimal_temperature_max__gte=temperature,
        optimal_humidity_min__lte=humidity,
        optimal_humidity_max__gte=humidity,
        optimal_soil_moisture_min__lte=soil_moisture,
        optimal_soil_moisture_max__gte=soil_moisture
    )
    return crops
def weather(request):
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather_data(city)
            if weather_data['cod'] == 200:
                sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')
                sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')
                temperature = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                # Assuming soil moisture data is available from another source or set a default value
                soil_moisture = 50  # Example default value
                recommended_crops = recommend_crops(temperature, humidity, soil_moisture)
                context = {
                    'city': city,
                    'temperature': temperature,
                    'description': weather_data['weather'][0]['description'],
                    'icon': weather_data['weather'][0]['icon'],
                    'humidity': humidity,
                    'wind_speed': weather_data['wind']['speed'],
                    'pressure': weather_data['main']['pressure'],
                    'sunrise': sunrise,
                    'sunset': sunset,
                    'visibility': weather_data['visibility'],
                    'feels_like': weather_data['main']['feels_like'],
                    'soil_moisture': soil_moisture,
                    'precipitation': weather_data.get('precipitation', 'N/A'),  # Example placeholder
                    'temperature_extremes': weather_data.get('temperature_extremes', 'N/A'),  # Example placeholder
                    'wind_gusts': weather_data.get('wind_gusts', 'N/A'),  # Example placeholder
                    'uv_index': weather_data.get('uv_index', 'N/A'),  # Example placeholder
                    'dew_point': weather_data.get('dew_point', 'N/A'),  # Example placeholder
                    'recommended_crops': recommended_crops,
                }
            else:
                context = {'error_message': 'City not found'}
            return render(request, 'weather_app/weather.html', context)
    else:
        form = WeatherForm()
    return render(request, 'weather_app/weather.html', {'form': form})

def home(request):
    products = ProductData.objects.all()[:5]
    blogs = AgriculturalPost.objects.all()[:3]
    return render(request, 'home.html', {'products': products, 'blogs': blogs})

def admin(request):
    return render(request, 'admin/index.html')

def health(request):
        return render (request, 'healthcare.html')
    

def submit_doctor_view(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)   
        if form.is_valid():
            form.save()   
            return redirect('success_url')  
    else:
        form = DoctorForm()  

    return render(request, 'submit_doctor.html', {'form': form})
def doctor_list(request):
    doctors = Doctor.fetch_all()  # Fetch all doctors
    paginator = Paginator(doctors, 10)  # Create a Paginator instance
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Get the specific page
    return render(request, 'doctor_list.html', {'page_obj': page_obj})
def doc_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)  # Retrieve the specific record
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)  # Bind form to the record
        if form.is_valid():
            form.save()  # Save the updated data
            return redirect('doctor_list')  # Redirect to the doctor list
    else:
        form = DoctorForm(instance=doctor)  # Pre-fill the form with the record's data
    
    return render(request, 'submit_doctor.html', {'form': form})

# Delete view for doctor
def doc_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)  # Retrieve the record
    if request.method == 'POST':  # Confirm deletion
        doctor.delete()  # Delete the record
        return redirect('doctor_list')  # Redirect to the doctor list
    return render(request, 'doc_delete.html', {'doctor': doctor})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
#Login

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_choice = request.POST.get('user_choice')  # Get the user choice from the form
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}!')

            # Get the 'next' URL from the GET request, or use the user choice for redirection
            next_url = request.GET.get('next', None)  # Get the 'next' parameter or None if not provided

            # If no 'next' URL, we use user_choice for redirection
            if not next_url:
                if user_choice == 'telemedics':
                    return redirect('telemedics_dashboard')
                elif user_choice == 'finance':
                    return redirect('finance_dashboard')
                elif user_choice == 'agriculture':
                    return redirect('agriculture_dashboard')
                else:
                    return redirect('home')  # Default redirect if no 'next' or user choice

            # If 'next' URL exists, redirect to the requested page
            return redirect(next_url)
        else:
            messages.info(request, f'Invalid credentials. Please try again or sign up.')

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'title': 'Log In'})
#Profile
def user_profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html',{'name':request.user})
    else:
        return HttpResponseRedirect('/login/')
    #Logout
def user_logout(request):
    messages.info(request, "You have successfully logged out."),
    logout(request)
    return HttpResponseRedirect('/login/')
def ask_openai(message):
    
    try:
        # Make the OpenAI API request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can update the model as needed
            messages=[{"role": "user", "content": message}],
        )
        return response.choices[0].message['content']
    except Exception as e:
        # Return an error response in case of any failure
        return str(e)

def chatbot(request):
    
    openai.api_key = settings.OPENAI_API_KEY,

    if request.method == 'POST':
        message = request.POST.get('message')
        if not message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Fetch the response from OpenAI
        response = ask_openai(message)

        # Save the chat in the database
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()

        return JsonResponse({'message': message, 'response': response})

    # If it's a GET request, render the page with chat history
    chats = Chat.objects.filter(user=request.user)
    return render(request, 'AI.html', {'chats': chats})
def add_cropping(request):
    if request.method == 'POST':
        form = CroppingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crop_list')
    else:
        form = CroppingForm()  # Initialize a new form for GET requests

    return render(request, 'weather_app/add_cropping.html', {'form': form})
def crops(request):
    crops = Croping.fetch_all()
    return render(request,'crop.html', {'crops':crops})
def crop_update(request, pk):
    crop = get_object_or_404(Croping, pk=pk)  # Retrieve the specific record
    if request.method == 'POST':
        form =  CroppingForm(request.POST, instance=crop)  # Bind form to the record
        if form.is_valid():
            form.save()  # Save the updated data
            return redirect('cropping')  # Redirect to the doctor list
    else:
        form = CroppingForm(instance=crop)  # Pre-fill the form with the record's data
    
    return render(request, 'weather_app/add_cropping.html', {'form': form})
def crop_delete(request,pk):
    crop=get_object_or_404(Croping,pk=pk)
    if request.method=='POST':
        crop.delete()
        return redirect('cropping')
    return render(request, 'weather_app/delete_crop.html', {'crop': crop})
    
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()  # Initialize a new form for GET requests

    return render(request, 'Product/Product.html', {'form': form})
def products(request):
    products = ProductData.objects.all()
    return render(request,'Product/index.html', {'products':products})
def blog(request):
    blogs = AgriculturalPost.objects.all()
    return render(request, 'Blog/Blog.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(AgriculturalPost, slug=slug)

    # Split the blog title into words
    title_words = blog.title.split()

    # Create a Q object for each word to search in the title
    query = Q()
    for word in title_words:
        query |= Q(title__icontains=word)

    # Fetch related posts based on title words, excluding the current post
    related_posts = AgriculturalPost.objects.filter(query).exclude(slug=blog.slug)[:6]

    return render(request, 'Blog/Blog_detail.html', {'blog': blog, 'related_posts': related_posts})

     
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs')
        else:
            return HttpResponseRedirect(request.path_info)  # Refresh the page to avoid double submission
    else:
        form = BlogForm()
    return render(request, 'Blog/Create.html', {'form': form})
def about(request):
    return render(request, 'AboutUs.html')    
def sendinquiry(request):
    if request.method == 'POST':
        form = Inquiry(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request, 'Form submitted successfully!')
           return redirect('home')
        else:
         return HttpResponseRedirect(request.path_info)
    else:
         form = Inquiry()
         return render(request, 'inquiry.html', {'form': form})
def contact(request):
    if request.method == 'POST':
        form = Inquiry(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submitted successfully!')
            return redirect('products')
        else:
            return HttpResponseRedirect(request.path_info)
    else:
        form = Inquiry()
        return render(request, 'Contact.html', {'form': form})
# pestcheck/views.py
def pest_forecast_view(request):
    forecast_data = None
    coordinates = None
    crop = None

    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            crop = form.cleaned_data['crop']
            lat, lon = get_coordinates(location)
            if lat is not None and lon is not None:
                coordinates = {'latitude': lat, 'longitude': lon}
                forecast_data = get_pest_forecast(lat, lon, crop)
            else:
                forecast_data = {'error': "Could not fetch coordinates for the location."}
    else:
        form = LocationForm()

    return render(request, 'pestcheck/pest_forecast.html', {
        'form': form,
        'forecast': forecast_data,
        'coordinates': coordinates,
        'crop': crop
    })
 