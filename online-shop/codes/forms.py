from django import forms
from django.forms import ModelForm
from .models import Order, Product, Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields= '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields= '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'description': 'Description',
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields= ['username','email','password1','password2']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields= '__all__'
        exclude = ['user']
