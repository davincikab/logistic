from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, UserProfile, ShopOwner, Employee

class ShopOwnerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "password1", "password2")
        exclude = ('first_name', 'last_name')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_agency = True
        return user

class EmployeeSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_landlord = True
        return user

class ShopOwnerForm(forms.ModelForm):
    class Meta:
        model = ShopOwner
        fields = ("account_name", "location", "geom")

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", max_length=50, required=False)
    last_name = forms.CharField(label="Last Name", max_length=50, required=False)
    surname = forms.CharField(label="Surname", max_length=50, required=False)
    email = forms.EmailField(label="Email", required=False)
    phone_number = forms.CharField(
        label="Phone Number", max_length=13, required=False,
        help_text="Phone Number format: 254700111222",
        widget=forms.TextInput(attrs={
            'placeholder':'254700111222',
            'pattern':r'254[0-9]{9}'
        })
    )

    location = forms.CharField(label="Location", max_length=50, required=True)
    geom = forms.CharField(label="Point", max_length=255, required=True, 
        widget=forms.TextInput(attrs={
            'readonly':True
        })
    )

    account_name = forms.CharField(label="Shop Name", max_length=50, required=True)
    
    class Meta:
        model = UserProfile
        fields = ['image', 'phone_number']