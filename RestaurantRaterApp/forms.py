import os
from django import forms
from django.db import models
from django.core.exceptions import ValidationError

from RestaurantRater import settings
from RestaurantRaterApp.models import Restaurant, user_client
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django_resized import ResizedImageField
from django.core.files.storage import FileSystemStorage

current_dir = os.getcwd()


def validate_positive(value):
    if value < 0:
        raise ValidationError(f"{value} is not a positive number.")


# User creation form
class UserForm(forms.ModelForm):
    class Meta:
        model = User

        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control form-control-sm mb-2", 'id': 'id_username'}),
            'password': forms.PasswordInput(attrs={'class': "form-control form-control-sm mb-2 ", 'id': 'id_password'}),
            'email': forms.EmailInput(attrs={'class': "form-control form-control-sm mb-2 ", 'id': 'id_email'}),
        }

        fields = ('username', 'password', 'email',)


# User profile form
class SignUpForm(forms.ModelForm):
    class Meta:
        model = user_client

        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control form-control-sm mb-2", 'id': 'id_name'}),
            'surname': forms.TextInput(attrs={'class': "form-control form-control-sm mb-2 ", 'id': 'id_surname'}),
            'city': forms.TextInput(attrs={'class': "form-control form-control-sm mb-2 ", 'id': 'id_city'}),
            'street': forms.TextInput(attrs={'class': "form-control form-control-sm mb-2 "}),
            'street_number': forms.NumberInput(attrs={'class': "form-control form-control-sm mb-2 "}),
        }

        fields = ('name', 'surname', 'city', 'street', 'street_number')


# Edits the user model in user_client
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User

        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control form-control-sm mb-2 ",'id': 'id_username'}),
            'email': forms.EmailInput(attrs={'class': "form-control form-control-sm mb-2 ",'id': 'id_email'}),
        }

        fields = ('username', 'email',)


# Edits the user_client form
class EditSignUpForm(forms.ModelForm):
    class Meta:
        model = user_client

        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control form-control-sm mb-2",'id': 'id_name'}),
            'surname': forms.TextInput(attrs={'class': "form-control form-control-sm mb-2 ",'id': 'id_surname'}),
            'city': forms.TextInput(attrs={'class': "form-control form-control-sm mb-2 ",'id': 'id_city'}),
            'street': forms.TextInput(attrs={'class': "form-control form-control-sm mb-2 ",'id': 'id_street'}),
            'street_number': forms.TextInput(attrs={'class': "form-control form-control-sm mb-2 ",'id': 'id_st_number'}),
        }

        fields = ('name', 'surname', 'city', 'street', 'street_number')


class RestaurantForm(forms.ModelForm):
    name = forms.CharField(required=True)
    street_number = forms.IntegerField(required=True)
    street = forms.CharField(required=True)
    city = forms.CharField(required=True)
    description = forms.CharField(required=True)
    restaurant_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    fs = FileSystemStorage(location=settings.MEDIA_DIR)
    img1 = ResizedImageField(size=[225, 225], quality=100, crop=["middle", "center"],
                             storage=fs, force_format='jpeg', blank=True)
    img2 = ResizedImageField(size=[225, 225], quality=100, crop=["middle", "center"],
                             storage=fs, force_format='jpeg', blank=True)
    img3 = ResizedImageField(size=[225, 225], quality=100, crop=["middle", "center"],
                             storage=fs, force_format='jpeg', blank=True)
    comments = forms.CharField(widget=forms.HiddenInput(), required=False)
    ratings = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Restaurant
        fields = (
            'name', 'street_number', 'street', 'city', 'ratings', 'description', 'img1', 'img2', 'img3',
            'restaurant_id',
            'comments')


class ReviewForm(forms.ModelForm):
    STAR_CHOICES = [(0.5, '0.5 Stars'), (1, '1 Star'), (1.5, '1.5 Stars'), (2, '2 Stars'), (2.5, '2.5 Stars'),
                    (3, '3 Stars'),
                    (3.5, '3.5 Stars'), (4, '4 Stars'), (4.5, '4.5 Stars'), (5, '5 Stars')]
    rating = forms.CharField(label="Star Rating", widget=forms.Select(choices=STAR_CHOICES, attrs={
        'class': "form-control form-control-sm mb-2"}))
    review = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': "form-control form-control-sm mb-2", 'rows': 5, 'cols': 5}))

    class Meta:
        model = Restaurant
        fields = ('review',)
