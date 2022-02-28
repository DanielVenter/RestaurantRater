import os

from django.db import models
current_dir = os.getcwd()
from django.template.defaultfilters import slugify


class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    street_number = models.PositiveIntegerField()
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    map_link = models.CharField(max_length=256)
    ratings = models.JSONField(default=[])
    description = models.CharField(max_length=1500)
    img1 = models.ImageField(upload_to=f"{current_dir}\\media\\")
    img2 = models.ImageField(upload_to=f"{current_dir}\\media\\")
    img3 = models.ImageField(upload_to=f"{current_dir}\\media\\")
    restaurant_id = models.CharField(max_length=128, primary_key=True)
    comments = models.JSONField(default={})

    @property
    def rating(self):
        return sum(self.ratings) / len(self.ratings)

    def generate_map_link(self):
        self.map_link = f"{self.street_number}+{self.street}+{self.city}"
        self.map_link.replace(" ", "+")

    def __str__(self):
        return self.restaurant_id


class user_client(models.Model):
    username = models.CharField(max_length=128, primary_key=True)
    liked_restaurants = models.ManyToManyField(Restaurant, related_name="likes")
    street_number = models.PositiveIntegerField()
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    rated_restaurants = models.JSONField(default={})
    rates = models.ManyToManyField(Restaurant, related_name="rates")
    password = models.CharField(max_length=24)
    email = models.EmailField()
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    owner_status = models.BooleanField(default=False)
    owned_restaurants = models.ManyToManyField(Restaurant, related_name="owns")

    @property
    def owned_restaurants_list(self):
        owned_restaurants = []
        for restaurant in user_client.owned_restaurants.all():
            owned_restaurants.append(restaurant.name)
        return owned_restaurants

    @property
    def map_link(self):
        map_link = f"{self.street_number}+{self.street}+{self.city}"
        map_link.replace(" ", "+")
        return map_link

    def __str__(self):
        return self.username



