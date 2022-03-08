import os
import requests
import urllib.parse

from django.db import models
# copied from ae1 rango project to simulate user authentication (for testing only)
from django.contrib.auth.models import User
from django_resized import ResizedImageField

current_dir = os.getcwd()
API_KEY = "AIzaSyAxJa_f1f5FhqyY_JhZ42JBijy4dXNgGQA"


class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    street_number = models.PositiveIntegerField()
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    ratings = models.JSONField(default=list)
    description = models.CharField(max_length=240)
    img1 = ResizedImageField(size=[225, 225], quality=100, crop=["middle", "center"], upload_to=f"{current_dir}\\media\\", force_format='jpeg')
    img2 = ResizedImageField(size=[225, 225], quality=100, crop=["middle", "center"], upload_to=f"{current_dir}\\media\\", force_format='jpeg')
    img3 = ResizedImageField(size=[225, 225], quality=100, crop=["middle", "center"], upload_to=f"{current_dir}\\media\\", force_format='jpeg')
    restaurant_id = models.CharField(max_length=128, primary_key=True)
    comments = models.JSONField(default=dict)

    @property
    # Average rating that gets displayed to users.
    def rating(self):
        return round(sum(self.ratings) / len(self.ratings), 2)

    @property
    # Map Link used for Google API
    def map_link(self):
        map_address = f"{self.street_number}+{self.street.replace(' ', '+')},{self.city}"
        map_link = f"https://www.google.com/maps/embed/v1/place?key={API_KEY}&q={map_address}"
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
        map_address = f"{self.street_number}+{self.street.replace(' ', '+')},{self.city}"
        map_link = f"www.google.com/maps/embed/v1/place?key={API_KEY}&q={map_address}"
        return map_link

    @property
    # Generate distances to all the restaurants around them
    def distances_dict(self):
        distances = {}
        user = user_client.objects.get(username=self.username)
        start = f"{user.street_number} {user.street} {user.city}"
        for restaurant in Restaurant.objects.all():
            end = f"{restaurant.street_number} {restaurant.street} {restaurant.city}"
            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={urllib.parse.quote(start)}&destinations={urllib.parse.quote(end)}&departure_time=now&key={API_KEY}"

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            data = eval(response.text)
            distance = float(data["rows"][0]["elements"][0]["distance"]["text"].split(" ")[0])
            distances[restaurant.restaurant_id] = distance

        return distances

    def __str__(self):
        return self.username

# copied from ae1 rango project to simulate user authentication (for testing only)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username