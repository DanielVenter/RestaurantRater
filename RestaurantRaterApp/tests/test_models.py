from django.test import TestCase
from RestaurantRaterApp.models import user_client, Restaurant
from populate_database import populate_test

API_KEY = "AIzaSyAxJa_f1f5FhqyY_JhZ42JBijy4dXNgGQA"


class UserModelTests(TestCase):
    def setUp(self):
        populate_test()
        self.user = user_client.objects.get(name="Mark")
        self.user2 = user_client.objects.get(name="Nicola")

    # Tests user_client's __str__ method
    def test_user_str(self):
        msg = "user_client's string representation does not work accordingly"

        self.assertEqual(str(self.user), "Mark.E", msg)

    # Tests user_client's map_link property
    def test_map_link(self):
        msg = "user_client's map link does not work accordingly."

        self.assertEqual(self.user.map_link,
                         f"https://www.google.com/maps/embed/v1/place?key={API_KEY}&q=21+Beith+Street,Glasgow", msg)

    # Tests if user_client's owned_restaurants method returns a list of the corresponding size
    def test_owned_restaurants_list_len(self):
        msg = "user_client's owned restaurants list does not work accordingly"

        self.assertEqual(len(self.user.owned_restaurants_list), 0, msg)
        self.assertEqual(len(self.user2.owned_restaurants_list), 1, msg)

    # Tests if user_client's owned_restaurants method returns the list in the correct order
    def test_owned_restaurants_list_order(self):
        msg = "user_client's owned restaurants list does not work accordingly"

        self.assertEqual(f"{self.user2.owned_restaurants_list[0]}", "alchemilla", msg)

    # Tests if user_client's owned_restaurants returns the exact list
    def test_owned_restaurants_list_correct_list(self):
        msg = "user_client's owned restaurants list does not work accordingly"
        restaurant_ids = [Restaurant.objects.get(restaurant_id="alchemilla")]

        for restaurant_id in restaurant_ids:
            self.assertTrue(restaurant_id in self.user2.owned_restaurants_list, msg)

    # Tests distances_dictionary
    def test_user_dict(self):
        msg = "user distance dict not generated correctly"
        self.assertEqual(self.user.distances_dict,
                         {'alchemilla': 1.6, 'kimchi-cult': 0.9}, msg)

class RestaurantModelTests(TestCase):
    def setUp(self):
        populate_test()

        self.restaurant = Restaurant.objects.get(restaurant_id="alchemilla")

    # Tests Restaurant's __str__ method
    def test_restaurant_str(self):
        msg = "restaurant's string representation does not work accordingly"

        self.assertEqual(str(self.restaurant), "alchemilla", msg)

    # Tests if Restaurant's map_link property returns the correct link
    def test_restaurant_map_link(self):
        msg = "restaurant's map link does not work accordingly."

        self.assertEqual(self.restaurant.map_link,
                         f"https://www.google.com/maps/embed/v1/place?key={API_KEY}&q=1126+Argyle+Street,Glasgow", msg)

    # Tests if Restaurant's rating property computes the rating correctly.
    def test_restaurant_rating(self):
        msg = "restaurant's rating method does not work accordingly."

        self.assertEqual(self.restaurant.rating, 4, msg)
