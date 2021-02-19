from django.urls import path
from .views import home, map_view, shops_data, list_orders, create_order, create_product, order_details, vehicle_list

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", home, name="home"),
    path("map/", map_view, name="map"),
    path("shops-data", shops_data, name="shops-data"),
    path("list-orders/", list_orders, name="order"),
    path("create-order/", create_order, name="create-order"),
    path("order-details/<str:order_id>/", order_details, name="order-details"),
    path("add-product/<str:order_id>/", create_product, name="add-product"),

    path('vehicle-list/', vehicle_list, name="vehicle-list"),
] 


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   