from django.contrib import admin


from leaflet.admin import LeafletGeoAdmin

from .models import Customers, OrderProduct, Order, Route, Vehicle

# Register your models here.
admin.site.register(Customers, LeafletGeoAdmin)
@admin.register(Order)
class OrderAdmin(LeafletGeoAdmin):
    list_display = ('order_id', 'shop_keeper', 'is_delivered', 'vehicle',)


admin.site.register(OrderProduct)
admin.site.register(Route)
admin.site.register(Vehicle)