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
    card_number = forms.CharField(label='Card Number', required=True)
    card_expiry = forms.CharField(label='Card Expiry', required=True)
    card_cvv = forms.CharField(label='Card CVV', required=True)
