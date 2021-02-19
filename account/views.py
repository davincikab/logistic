from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.contrib import messages

from .forms import EmployeeSignUpForm, ShopOwnerSignUpForm, ProfileForm, ShopOwnerForm
from .models import User, UserProfile, ShopOwner, Employee
from logistic.models import Order

def signup(request):
    return render(request, "account/signup.html")

class EmployeeSignUpView(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = "account/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs['user_type'] = 'landlord'
        context['title'] = "Employee Registration"
        context['submit'] = "Register"
       
        return context
    
    def form_valid(self, form):
        user = form.save()
        user.is_employee = True
        user.save()

        login(self.request, user)
        messages.success(self.request, "Account Successfully Created")

        return redirect('profile')
        

class ShopOwnerSignUpView(CreateView):
    model = User
    form_class = ShopOwnerSignUpForm
    template_name = "account/register.html"    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs['user_type'] = 'agency'
        context['title'] = "Shop Registration "
        context['submit'] = "Register Your Shop"

        return context
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_shopowner = True
        user.save()
        
        login(self.request, user)

        messages.success(self.request, "Account Successfully Created")
        return redirect('profile')
   

# profile view
class ProfileCreateView(LoginRequiredMixin, FormView):
    login_url = "/user/login/"
    model = UserProfile
    form_class = ProfileForm
    template_name = "account/create_profile.html"
    success_url = "/account/profile"     

    def get_initial(self):  
        user = User.objects.get(username = self.request.user.username)
        try:
            profile = UserProfile.objects.get(user=self.request.user)

            # get plot info 

            profile = {**model_to_dict(profile), **model_to_dict(user)}
        except UserProfile.DoesNotExist:
            profile = model_to_dict(user)
        
        return profile
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        profile = form.save(commit=False)

        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
            form = self.form_class(self.request.POST or None, self.request.FILES, instance=user_profile)
            form.save()
        except UserProfile.DoesNotExist:
            print(self.request.FILES)
            profile.user = self.request.user
            # profile.image = self.request.FILES
            profile.save()
            
           

        print('Valid')
        print(self.request.POST)
        user_details = self.request.user

        from operator import itemgetter
        first_name, last_name, surname = itemgetter('first_name', 'last_name', 'surname')(self.request.POST)

        user_details.first_name = first_name
        user_details.last_name = last_name
        user_details.surname = surname

        user_details.save()

        # update account name, geom and location
        if self.request.user.is_shopowner:
            print(self.request.POST)
            shopowner = ShopOwner.objects.get(user=self.request.user)
            shopowner.location = self.request.POST.get('location')
            shopowner.geom = self.request.POST.get('geom')
            shopowner.account_name = self.request.POST.get('account_name')

            shopowner.save()

        return redirect(self.success_url)
    
    def form_invalid(self, form):
        print(form)
        print(form.errors)
        return HttpResponse("Invalid data")

class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/account/login/' 
    template_name = "account/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            username = self.request.GET.get('user', None)
            # print(User.objects.get(username=user))
            if username:
                context['profile'] = UserProfile.objects.get(user__username=username)
                context['active_orders'] = Order.objects.filter(shop_keeper=self.request.user)
            else:
                context['profile'] = UserProfile.objects.get(user=self.request.user)
                context['active_orders'] = Order.objects.filter(shop_keeper=self.request.user)
        except UserProfile.DoesNotExist or User.DoesNotExist:
            print("Failed")
            context["profile"] = {}
            context['active_orders'] = []
        
        return context
    
