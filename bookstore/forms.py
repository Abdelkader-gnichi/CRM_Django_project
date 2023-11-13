from typing import Any
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OrderForm(ModelForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs.update({'class':'form-control'})
        self.fields['book'].widget.attrs.update({'class':'form-control'})
        self.fields['status'].widget.attrs.update({'class':'form-control'})

        self.fields['customer'].empty_label = 'Press to select a Customer'
        self.fields['book'].empty_label = 'Press to select a Book'
        self.fields['status'].choices= [('','Press to select a Status')] + list(Order.STATUS)
       
    class Meta:
        model = Order
        fields = '__all__'

class CustomerForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs.update({'class':'form-control'})
        self.fields['address'].widget.attrs.update({'class':'form-control'})

    
    class Meta:
        model= Customer
        fields = "__all__"
        exclude = ['user']

class UserForm(ModelForm):
    class Meta:
        model= User
        fields=('first_name','last_name','username','email')


class RegisterForm(UserCreationForm):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'form-control','placeholder':'first name'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control','placeholder':'last name'})
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'username'})
        self.fields['email'].widget.attrs.update({'class':'form-control','placeholder':'email'})
        self.fields['password1'].widget.attrs.update({'class':'form-control','placeholder':'password'})
        self.fields['password2'].widget.attrs.update({'class':'form-control','placeholder':'password confirmation'})

    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')