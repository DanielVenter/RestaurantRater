import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RestaurantRater.settings')

import django

django.setup()
from rango.models import User, Restaurant


def populate():

    users = [{ "name" : "", "street_number" : "", "street" : "", "city" : " ", "map_link" : " ",
               "ratings" : ""

    },

    ]



    def add_restaurant:


    def add_user:



    def likes(User, Restaurant):


    def owns(User, Restaurant):


    def rates(User, Restaurant)