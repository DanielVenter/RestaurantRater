from django.test import TestCase
from populate_database import populate, likes, rates, owns
from RestaurantRaterApp.models import user_client, Restaurant


class PopulationScriptTests(TestCase):
    def setUp(self):
        populate()

    #Tests populate_database's likes method
    def test_likes(self):
        msg = "population script's likes method does not work accordingly."
        likes("Colin", "ALC")

        self.assertTrue(Restaurant.objects.get(restaurant_id="ALC") in user_client.objects.get(
            name="Colin").liked_restaurants.all(), msg)

    #Tests if populate_database's rates method adds the rating to the Restaurant's ratings list
    def test_rates_adds_rating_list_size(self):
        msg = "population script's rates method does not work accordingly"

        usr = user_client.objects.get(name="Colin")
        usr.rated_restaurants["ALC"] = 5
        usr.save()

        rates("Colin", "ALC")

        self.assertEqual(8, len(Restaurant.objects.get(restaurant_id="ALC").ratings), msg)

    #Tests if Restaurant's rating property calculates a new rating every time, even if the ratings list has changed
    def test_rates_adds_rating_calculation(self):
        msg = "population script's rates method does not work accordingly"

        usr = user_client.objects.get(name="Colin")
        usr.rated_restaurants["ALC"] = 5
        usr.save()

        rates("Colin", "ALC")
        self.assertEqual(4.38, Restaurant.objects.get(restaurant_id="ALC").rating, msg)

    #Tests if user_clients that are owners are assigned with at least one owned restaurant
    def test_owners_have_owned_restaurant(self):
        msg = "population script does not give owners at least one restaurant"

        lst = user_client.objects.all().filter(owner_status=True)

        for usr in lst:
            self.assertTrue(len(usr.owned_restaurants.all()) > 0, msg)

    #Tests if all user_clients that are not owners have no restaurants owned
    def test_not_owners_have_zero_restaurants(self):
        msg = "population script does give users that are not owners an empty list"

        lst = user_client.objects.all().filter(owner_status=False)

        for usr in lst:
            self.assertTrue(len(usr.owned_restaurants.all()) == 0, msg)

    #Tests if populate_database's owns method modifies the owned_restaurants list of the user
    def test_owns_len(self):
        msg = "population script's owns method does not work accordingly"

        owns("Danny", "ALC")

        self.assertTrue(len(user_client.objects.get(name="Danny").owned_restaurants.all()) == 6, msg)

    #Tests if populate_database's owns method adds the restaurant to the user's owned_restaurants list
    def test_owns_restaurant_added(self):
        msg = "population script's owns method does not work accordingly"

        owns("Danny", "ALC")

        self.assertTrue(Restaurant.objects.get(restaurant_id="ALC") in user_client.objects.get(
            name="Danny").owned_restaurants.all(), msg)

    #Tests if the population script creates a correct number of restaurants
    def test_correct_no_restaurants(self):
        msg = "population script does not create all restaurants."

        self.assertEqual(len(Restaurant.objects.all()), 15, msg)

    #Tests if the population script creates a correct number of users
    def test_correct_no_users(self):
        msg = "population script does not create all users."

        self.assertEqual(len(user_client.objects.all()), 11, msg)

    #Tests if the population script creates the correct restaurants
    def test_correct_restaurants_created(self):
        msg = "population script does not create all restaurants."

        restaurant_ids = ["ALC", "JK", "KC", "OnF", "BE", "CB", "HBS", "TG", "FM", "ST", "PDC", "N16", "SB", "B6", "GL"]

        for restaurant_id in restaurant_ids:
            self.assertIsNotNone(Restaurant.objects.get(restaurant_id=restaurant_id))

    #Tests if the population script creates the correct users
    def test_correct_users_created(self):
        msg = "population script does not create all users."

        usernames = ["Mark.E", "Thom.O", "Matt.W", "Michael.G", "Andy.P", "Rose.S", "Jeremy.S", "Jeff.D", "Colin",
                     "Nicola.H", "Danny.M"]

        for username in usernames:
            self.assertIsNotNone(user_client.objects.get(username=username))
