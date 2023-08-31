from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required')
    address = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=255)
    #account_type = forms.ChoiceField(choices=CustomUser.ACCOUNT_TYPES, required=True)

    class Meta:
        model = CustomUser
        fields = ('full_name', 'address', 'phone_number', 'email', 'password1', 'password2')


class CheckoutForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16)
    card_expiry = forms.CharField(label='Card Expiry', max_length=5)
    card_cvv = forms.CharField(label='Card CVV', max_length=3)
    full_name = forms.CharField(label='Full Name', max_length=100)
    address = forms.CharField(label='Address', max_length=100)
