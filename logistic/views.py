from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# 3rd party
import json
import uuid

# local files
from .decorators import employee_required, shopowner_required
from .models import Customers, Order, OrderProduct, Vehicle, Route
from .forms import OrderProductForm


def home(request):
    context = {
        'section':'home'
    }

    return render(request, "logistic/home.html", context)

@login_required
@user_passes_test(employee_required)
def map_view(request):
    context = {
        'section':'map'
    }

    return render(request, "logistic/map.html", context)

@user_passes_test(employee_required)
@login_required
def vehicle_views(request):
    context = {
        'section':'vehicle'
    }

    return render(request, "logistic/map.html", context)


# shops data
@user_passes_test(employee_required)
def shops_data(request):
    data = serialize('geojson', Customers.objects.all())
    return HttpResponse(json.dumps({'customers': data}))


# Orders
@login_required
def list_orders(request):
    if request.user.is_staff:
        if request.GET.get('query', None):
            query = request.GET.get('query')

            print(query)
            orders = Order.objects.filter(is_delivered=False).filter(shop_keeper__username__icontains=query)
        else:
            orders = Order.objects.filter(is_delivered=False)
    else:
        orders = Order.objects.filter(is_delivered=False).filter(shop_keeper=request.user)

    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    orders = paginator.get_page(page)

    context = {
        "orders":orders,
        "section":"orders"
    }

    return render(request, "logistic/order.html", context)

@csrf_exempt
@login_required
@user_passes_test(shopowner_required)
def create_order(request):
    if request.method == "POST": 
        unique_id = uuid.uuid4().hex[:6].upper()

        route = Route.objects.get(route_name__icontains=request.user.shopowner.location)
        vehicle = Vehicle.objects.get(route=route)

        print(route)

        order = Order.objects.create(
            order_id=unique_id, 
            shop_keeper=request.user,
            geom=request.user.shopowner.geom,
            vehicle=vehicle
        )

        context = {
            'message':'success',
            'url':f"/add-product/{order.order_id}/"
        }

        return HttpResponse(json.dumps(context))
    else:
        return HttpResponse(json.dumps({'message':'Failed'}))

@csrf_exempt
@login_required
@user_passes_test(shopowner_required)
def order_details(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    if request.method == "POST":
        print(request.POST)

        action = request.POST.get('action', None)
        print(action)

        if action == "delivery":
            print(action)
            order.is_delivered = True
            order.save()
        else:
            order.payment_status = True
            order.save()
        
        return HttpResponse(json.dumps({'message':'success'}))

    context  = {
        'order':order
    }

    return render(request, "logistic/order_detail.html", context)

@login_required
@user_passes_test(shopowner_required)
def create_product(request, order_id):
    order = Order.objects.get(order_id=order_id)

    if request.method == "POST":
        print(request.POST)

        # create list of items 
        item_names = request.POST.get('item_names')
        print(item_names)
        item_names = item_names.split(",")

        # create products
        OrderProduct.objects.bulk_create(
            [OrderProduct(order=order, item_name=name) for name in item_names]
        )

        res = {
            'message':"success",
            'status':"ok"
        }

        return HttpResponse(json.dumps(res))

    else:
        form = OrderProductForm()

    context = {
        'form':form,
        'order':order
    }

    return render(request, "logistic/product_add.html", context)


# List of vehicles
@login_required
@staff_member_required
def vehicle_list(request):
    if request.GET.get('query', None):
        query = request.GET.get('query')
        vehicles = Vehicle.objects.filter(number_plate__icontains=query)
    else:
        vehicles = Vehicle.objects.all()
    
    route = Route.objects.all()
    context = {
        'vehicles':vehicles
    }

    return render(request, "logistic/vehicle.html", context)


# CREATE AN ORDER
# ASSIGN A VEHICLE
# FILTER THE ORDER DETAILS AS PER THE Logged on user
# FILTER ORDERS BY ROUTE
# FILTER ORDERS BY VEHICLE

