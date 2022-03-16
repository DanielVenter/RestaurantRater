import requests
import urllib.parse
from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from RestaurantRater import settings
from django.core.files.storage import FileSystemStorage
from django.template.defaultfilters import slugify


API_KEY = "AIzaSyAxJa_f1f5FhqyY_JhZ42JBijy4dXNgGQA"

fs = FileSystemStorage(location=settings.MEDIA_DIR)

class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    street_number = models.PositiveIntegerField()
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    ratings = models.JSONField(default=list)
    description = models.CharField(max_length=240)
    img1 = ResizedImageField(size=[225, 225], quality=100, crop=["middle", "center"],
                             storage=fs, force_format='jpeg')
    img2 = ResizedImageField(size=[225, 225], quality=100, crop=["middle", "center"],
                             storage=fs, force_format='jpeg')
    img3 = ResizedImageField(size=[225, 225], quality=100, crop=["middle", "center"],
                             storage=fs, force_format='jpeg')
    restaurant_id = models.SlugField(max_length=128, primary_key=True)
    comments = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        self.restaurant_id = slugify(self.name)
        super(Restaurant, self).save(*args, **kwargs)

    @property
    # Average rating that gets displayed to users.
    def rating(self):
        try:
            return round(sum(self.ratings) / len(self.ratings), 2)
        except ZeroDivisionError:
            return 0

    @property
    # Map Link used for Google API
    def map_link(self):
        map_address = f"{self.street_number}+{self.street.replace(' ', '+')},{self.city}"
        map_link = f"https://www.google.com/maps/embed/v1/place?key={API_KEY}&q={map_address}"
        return map_link

    def __str__(self):
        return self.restaurant_id


class user_client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    liked_restaurants = models.ManyToManyField(Restaurant, related_name="likes", blank=True)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    street_number = models.PositiveIntegerField()
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    rated_restaurants = models.JSONField(default=dict)
    rates = models.ManyToManyField(Restaurant, related_name="rates", blank=True)
    owner_status = models.BooleanField(default=False)
    owned_restaurants = models.ManyToManyField(Restaurant, related_name="owns", blank=True)
    distances_dict = models.JSONField(default=dict)

    @property
    # List generated for easy checking
    def owned_restaurants_list(self):
        owned_restaurants = []
        for restaurant in self.owned_restaurants.all():
            owned_restaurants.append(restaurant)
        return owned_restaurants

    @property
    # MapLink used for Google APIs
    def map_link(self):
        map_address = f"{self.street_number}+{self.street.replace(' ', '+')},{self.city}"
        map_link = f"https://www.google.com/maps/embed/v1/place?key={API_KEY}&q={map_address}"
        return map_link

    # Updates/Generates distances to all the restaurants around them
    def update_distances_dict(self, new_address=False):
        user = user_client.objects.get(user=self.user)
        distances_matrix = user.distances_dict
        restaurants = []

        start = f"{user.street_number} {user.street} {user.city}"
        end = []

        if new_address:
            for restaurant in Restaurant.objects.all():
                end.append(f"{restaurant.street_number} {restaurant.street} {restaurant.city}")
                restaurants.append(f"{restaurant}")
        else:
            for restaurant in Restaurant.objects.all():
                if f"{restaurant}" not in user.distances_dict:
                    end.append(f"{restaurant.street_number} {restaurant.street} {restaurant.city}")
                    restaurants.append(f"{restaurant}")

        destinations = "|".join(end)

        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={urllib.parse.quote(start)}&destinations={urllib.parse.quote(destinations)}&departure_time=now&key={API_KEY}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        data = eval(response.text)
        distances = (data["rows"][0]["elements"])
        for i, distance in enumerate(distances):
            distances_matrix[restaurants[i]] = float(distance["distance"]["text"].split(" ")[0])
        user.distances_dict = distances_matrix
        user.save()

    def __str__(self):
        return self.user.username
