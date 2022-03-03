import requests
import urllib.parse
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RestaurantRater.settings')

import django

django.setup()

from RestaurantRaterApp.models import Restaurant, user_client

API_KEY = "AIzaSyAxJa_f1f5FhqyY_JhZ42JBijy4dXNgGQA"


def get_distance():
    matrix = {}

    for user in user_client.objects.all():
        distances = {}
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

        matrix[user.username] = distances

    return matrix

print(get_distance())