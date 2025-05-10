from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# from django.contrib.gis.db import models
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=20)
    
class Doctor(models.Model):
    name = models.CharField(max_length=191, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    specialty = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    research_area = models.TextField(blank=True, null=True)
    publications_count = models.PositiveIntegerField(default=0)
    date_joined = models.DateField()
    active = models.BooleanField(default=True)
    @classmethod
    def fetch_all(cls):
        return cls.objects.all()

    def __str__(self):
        return f"Dr. {self.name} - {self.specialty}"
class Condition(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'
class Croping(models.Model):
    name = models.CharField(max_length=100)
    optimal_temperature_min = models.FloatField()
    optimal_temperature_max = models.FloatField()
    optimal_humidity_min = models.FloatField()
    optimal_humidity_max = models.FloatField()
    optimal_soil_moisture_min = models.FloatField()
    optimal_soil_moisture_max = models.FloatField()
    image_url = models.URLField(max_length=200, null=True, blank=True) 
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    @classmethod 
    def fetch_all(cls):
       return cls.objects.all()
class ProductData(models.Model):
    EQUIPMENT = 'equipment'
    SEEDLING = 'seedling'
    OTHER = 'other'

    PRODUCT_TYPE_CHOICES = [
        (EQUIPMENT, 'Equipment'),
        (SEEDLING, 'Seedling'),
        (OTHER, 'Other'),
    ]

    product_name = models.CharField(max_length=255)
    product_type = models.CharField(
        max_length=50,
        choices=PRODUCT_TYPE_CHOICES,
        default=OTHER,
        help_text="Type of product: Equipment, Seedling, or Other"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    warranty_period = models.IntegerField(blank=True, null=True, help_text="Warranty period in months (for equipment)")
    seed_type = models.CharField(max_length=100, blank=True, null=True, help_text="Type of seedling (e.g., vegetable, fruit, grain)")
    growth_duration = models.IntegerField(blank=True, null=True, help_text="Growth duration in days (for seedlings)")
    available_quantity = models.IntegerField(help_text="Available quantity in stock")
    description = models.TextField(blank=True, null=True, help_text="Additional details or product description")
    location = models.CharField(max_length=255, help_text="Location of the product")
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)  # New column
    def __str__(self):
        return f"{self.product_name} ({self.product_type})"

    class Meta:
        verbose_name = "Agricultural Product"
        verbose_name_plural = "Agricultural Products"
        
class AgriculturalPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    pub_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(default='default-slug')

def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while AgriculturalPost.objects.filter(slug=self.slug).exists():
                # Append a numeric suffix to make the slug unique
                suffix = 1
                original_slug = self.slug
                while AgriculturalPost.objects.filter(slug=self.slug).exists():
                    self.slug = f"{original_slug}-{suffix}"
                    suffix += 1
        super(AgriculturalPost, self).save(*args, **kwargs)
class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inquiry from {self.name} ({self.email})"