from django.dispatch import receiver
from django.db.models.signals import post_save


from .models import User, UserProfile, Employee, ShopOwner

@receiver(post_save, sender=User)
def create_pprofile(sender, instance, created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

        if instance.is_employee:
            # create agency instance
            Employee.objects.create(user=instance)
        
        if instance.is_shopowner:
            # create lanlord instance
            ShopOwner.objects.create(user=instance)