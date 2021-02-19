from django.contrib import admin
from .models import User, Employee, Contact, UserProfile, ShopOwner

# Register your models here.
admin.site.register(User)
admin.site.register(ShopOwner)
admin.site.register(Contact)
admin.site.register(UserProfile)
admin.site.register(Employee)

