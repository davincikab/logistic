from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

from account.models import Employee

User = get_user_model()

class Customers(models.Model):
    geom = models.PointField(blank=True, null=True)
    date = models.CharField(max_length=20, blank=True, null=True)
    route_code = models.CharField(db_column='route code', max_length=60, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    route_name = models.CharField(db_column='route name', max_length=60, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    account_number = models.IntegerField(db_column='account number', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    account_name = models.CharField(db_column='account name', max_length=60, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    location = models.CharField(max_length=100, blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'

class Route(models.Model):
    route_code = models.CharField("Route Code", max_length=34)
    route_name = models.CharField("Route Name", max_length=50)
    
    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"

    def __str__(self):
        return self.route_code

    # def get_absolute_url(self):
    #     return reverse("Route_detail", kwargs={"pk": self.pk})

class Vehicle(models.Model):
    number_plate = models.CharField("Number Plate", max_length=50)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    driver = models.ForeignKey(Employee, on_delete=models.CASCADE)    

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return self.number_plate

    # def get_absolute_url(self):
    #     return reverse("Vehicle_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    shop_keeper = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id =  models.CharField("Order Id", max_length=12)
    created_on = models.DateTimeField("Created On", auto_now=True)
    is_delivered = models.BooleanField("Delivery Status", default=False)
    payment_status = models.BooleanField("Paid", default=False)
    geom = models.PointField(blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.order_id

    # def get_absolute_url(self):
    #     return reverse("Order_detail", kwargs={"pk": self.pk})

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_name = models.CharField("Item", max_length=100)
    # cost = models.IntegerField()
    
    class Meta:
        verbose_name = "OrderProduct"
        verbose_name_plural = "OrderProducts"

    def __str__(self):
        return self.item_name

    # def get_absolute_url(self):
    #     return reverse("OrderProduct_detail", kwargs={"pk": self.pk})


