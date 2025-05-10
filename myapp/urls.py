from django.contrib import admin
from django.urls import path
from . import views  # Import your app's views
from django.contrib.auth import views as auth
from django.contrib.auth import views as auth_views
from .views import pest_forecast_view

urlpatterns = [
    # path('admin/', admin.site.urls),
        path('registeration/', views.register, name='register'),
        path('login/', views.Login, name='login'),
     path('profile/',views.user_profile,name='profile'),
         path('logout/',views.user_logout,name='logout'),

    path('', views.home, name='home'),  
    path('admins/',views.admin,name='admin'),
    path('telemedics_dashboard/', views.health, name='telemedics_dashboard'),
    path('submit-doctors/', views.submit_doctor_view, name='submit_doctor'),
    path('doctors/',views.doctor_list,name='doctor_list'),
    path('doctor/<int:pk>/edit/', views.doc_update, name='doctor_edit'),  # Edit URL
    path('doctor/<int:pk>/delete/', views.doc_delete, name='doctor_delete'), # Delete URL
    path('ai/',views.chatbot,name="ai"),
    path('weather/',views.weather,name='weather'),
    path('add_cropping/',views.add_cropping,name="add_cropping"),
    path('crops',views.crops,name="cropping"),
    path('crop_update<int:pk>/update',views.crop_update,name="crop_update"),
    path('delete_crop<int:pk>/delete',views.crop_delete,name="crop_delete"),
    path('create_products/',views.add_product,name="add_product"),
    path('products/',views.products,name="products"),
    path('blogs/',views.blog,name="blogs"),
    path('add_blog/',views.add_blog,name="add_blog"),
     path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),
     path('about/',views.about,name="about"),
     path('inquiry/',views.sendinquiry,name="inquiry"), 
     path('contacts/',views.contact,name="contacts"),
    path('forecast/', pest_forecast_view, name='pest_forecast'),

     
     # path('satelite', views.satellite_images, name='satellite_images'),
    ]
