import os
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from RestaurantRaterApp.models import UserProfile, Restaurant, user_client
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
current_dir = os.getcwd()

def validate_positive(value):
    if value < 0:
        raise ValidationError(f"{value} is not a positive number.")

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password', )

class SignUpForm(forms.ModelForm):
    class Meta:
        model = user_client
        fields = ('city', 'street', 'street_number')

class EditForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class RestaurantForm(forms.ModelForm):
    name = forms.CharField(required=True)
    street_number = forms.IntegerField(required=True)
    street = forms.CharField(required=True)
    city = forms.CharField(required=True)
    description = forms.CharField(required=True)
    img1 = models.ImageField(f"{current_dir}\\media\\")
    img2 = models.ImageField(f"{current_dir}\\media\\")
    img3 = models.ImageField(f"{current_dir}\\media\\")
    restaurant_id = forms.IntegerField(required=True)
    comments = forms.CharField(required=True)

    class Meta:
        model = Restaurant
        fields = ('name', 'street_number', 'street', 'city', 'ratings', 'description', 'img1','img2', 'img3', 'restaurant_id', 'comments')

class ReviewForm(forms.ModelForm):
    review = forms.CharField(required=True)
    class Meta:
        model = Restaurant
        fields = ('review',)