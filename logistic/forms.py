from django import forms

from .models import OrderProduct, Order

# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         exclude = "__all__"

class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ("item_name",)

