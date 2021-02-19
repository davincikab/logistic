from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser

from PIL import Image

# Create your models here.
class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_shopowner = models.BooleanField(default=False)
    date_joined = models.DateTimeField("Date Joined", auto_now=True)
    phone_number = models.CharField("Phone Number", max_length=13)
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

# class landlord
class Employee(models.Model):
    ROLE = (
        ('Driver', 'Driver'),
        ('General Labourer', 'General Labourer'),
        ('Supervisor', 'Supervisor'),
        ('Supervisor', 'Supervisor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField('Role', max_length=50, choices=ROLE)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employee"

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse("Landlord_detail", kwargs={"pk": self.pk})

class ShopOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.IntegerField(unique=True, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    account_name = models.CharField("Shop Name", max_length=60, blank=True, null=True)  
    location = models.CharField("Location", max_length=50, blank=True)
    geom = models.PointField(srid=4326, blank=True, null=True)

    class Meta:
        verbose_name = "ShopOwner"
        verbose_name_plural = "ShopOwner"
    
    def __str__(self):
        return self.user.username
    


# Contacts Model
class Contact(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    phone_number = models.CharField("Phone Number", max_length=13)
    email = models.EmailField("Email", max_length=254)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.user.username
    # def get_absolute_url(self):
    #     return reverse("Contact_detail", kwargs={"pk": self.pk})

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField("Profile Picture", upload_to="profile_picture", default="user.jpg")

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.image.path)

        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)

# TODO: add geometry to users, location name (CHOICES), 
# Automatically assign a user a route (depending on the location name), code, route name, account_name
# 