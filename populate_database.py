import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RestaurantRater.settings')

import django

django.setup()
from rango.models import User, Restaurant


def add_restaurant(name, street_number, street, city, description, id, comments):
    r = Restaurant.objects.get_or_create(name=name, ID=id)[0]
    r.street_number = street_number
    r.street = street
    r.city = city
    r.description = description
    r.get_next_in_order()
    r.comments = comments


def add_user(username, street_number, street, city, liked_restaurants, rated_restaurants, password, email, name,
             surname,
             owner_status=False, owned_restaurants=[]):
    u = User.objects.get_or_create(username=username)[0]
    u.street_number = street_number
    u.street = street
    u.city = city
    u.rated_restaurants = rated_restaurants
    u.password = password
    u.email = email
    u.name = name
    u.surname = surname
    u.owner_status = owner_status

    # Adds ratings
    for restaurant in rated_restaurants.keys():
        rates(name, restaurant)

    # Adds liked restaurants
    for restaurant in liked_restaurants:
        likes(name, restaurant)

    # Adds Owner's Restaurants
    if owner_status:
        for restaurant in owned_restaurants:
            owns(name, restaurant)


def rates(user, restaurant):
    user_obj = User.objects.get(name=user)
    restaurant_obj = Restaurant.objects.get(name=restaurant)
    restaurant_obj.ratings.add(user_obj)


def owns(user, restaurant):
    user_obj = User.objects.get(name=user)
    restaurant_obj = Restaurant.objects.get(name=restaurant)
    user_obj.owned_restaurants.add(restaurant_obj)


def likes(user, restaurant):
    user_obj = User.objects.get(name=user)
    restaurant_obj = Restaurant.objects.get(name=restaurant)
    user_obj.liked_restaurants.add(restaurant_obj)


def populate():
    restaurant_data = [
        {"name": "",
         "street_number": "",
         "street": "",
         "city": " ",
         "description": "",
         "id": " ",
         "comments": {}}]

    user_data = [
        {"username": "",
         "street_number": "",
         "street": "",
         "city": "",
         "liked_restaurants": [],
         "rated_restaurants": {},
         "password": "",
         "email": "",
         "name": "",
         "surname": "",
         "owner_status": False,
         "owned_restaurants": []
         }
    ]
