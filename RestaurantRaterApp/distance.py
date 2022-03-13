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
    end = []
    restaurants =[]
    for restaurant in Restaurant.objects.all():
        end.append(f"{restaurant.street_number} {restaurant.street} {restaurant.city}")
        restaurants.append(f"{restaurant}")

    print(restaurants)
    destinations = "|".join(end)

    for user in user_client.objects.all():
        distances_dict = {}
        print(user)
        start = f"{user.street_number} {user.street} {user.city}"
        ends = urllib.parse.quote(destinations)

        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={urllib.parse.quote(start)}&destinations={ends}&departure_time=now&key={API_KEY}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        data = eval(response.text)
        distances = (data["rows"][0]["elements"])
        for i, distance in enumerate(distances):
            distances_dict[restaurants[i]] =(distance["distance"]["text"].split(" ")[0])

        print(distances_dict)







print(get_distance())