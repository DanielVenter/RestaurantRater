import os

from django.db import models
# copied from ae1 rango project to simulate user authentication (for testing only)
from django.contrib.auth.models import User

current_dir = os.getcwd()


class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    street_number = models.PositiveIntegerField()
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    ratings = models.JSONField(default=list)
    description = models.CharField(max_length=1500)
    img1 = models.ImageField(upload_to=f"{current_dir}\\media\\")
    img2 = models.ImageField(upload_to=f"{current_dir}\\media\\")
    img3 = models.ImageField(upload_to=f"{current_dir}\\media\\")
    restaurant_id = models.CharField(max_length=128, primary_key=True)
    comments = models.JSONField(default=dict)

    @property
    def rating(self):
        return round(sum(self.ratings) / len(self.ratings), 2)

    @property
    # Map Link used for Google API
    def map_link(self):
        map_link = f"{self.street_number}+{self.street.replace(' ', '+')}+{self.city}"
        return map_link

    def __str__(self):
        return self.restaurant_id


class user_client(models.Model):
    username = models.CharField(max_length=128, primary_key=True)
    liked_restaurants = models.ManyToManyField(Restaurant, related_name="likes")
    street_number = models.PositiveIntegerField()
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    rated_restaurants = models.JSONField(default=dict)
    rates = models.ManyToManyField(Restaurant, related_name="rates")
    password = models.CharField(max_length=24)
    email = models.EmailField()
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    owner_status = models.BooleanField(default=False)
    owned_restaurants = models.ManyToManyField(Restaurant, related_name="owns")

    @property
    # List generated for easy checking
    def owned_restaurants_list(self):
        owned_restaurants = []
        for restaurant in self.owned_restaurants.all():
            owned_restaurants.append(restaurant.restaurant_id)
        return owned_restaurants

    @property
    # MapLink used for Google APIs
    def map_link(self):
        map_link = f"{self.street_number}+{self.street.replace(' ', '+')}+{self.city}"
        return map_link

    def __str__(self):
        return self.username

# copied from ae1 rango project to simulate user authentication (for testing only)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username