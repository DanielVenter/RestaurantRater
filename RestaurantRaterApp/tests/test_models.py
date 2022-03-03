from django.test import TestCase
from RestaurantRaterApp.models import user_client, Restaurant
from populate_database import populate


class UserModelTests(TestCase):
    def setUp(self):
        populate()
        self.user = user_client.objects.get(name="Mark")
        self.user2 = user_client.objects.get(name="Nicola")

    #Tests user_client's __str__ method
    def test_user_str(self):
        msg = "user_client's string representation does not work accordingly"

        self.assertEqual(str(self.user), "Mark.E", msg)

    #Tests user_client's map_link property
    def test_map_link(self):
        msg = "user_client's map link does not work accordingly."

        self.assertEqual(self.user.map_link, "21+Beith+Street+Glasgow", msg)

    #Tests if user_client's owned_restaurants method returns a list of the corresponding size
    def test_owned_restaurants_list_len(self):
        msg = "user_client's owned restaurants list does not work accordingly"

        self.assertEqual(len(self.user.owned_restaurants_list), 0, msg)
        self.assertEqual(len(self.user2.owned_restaurants_list), 5, msg)

    #Tests if user_client's owned_restaurants method returns the list in the correct order
    def test_owned_restaurants_list_order(self):
        msg = "user_client's owned restaurants list does not work accordingly"

        self.assertEqual(self.user2.owned_restaurants_list[0], "B6", msg)

    #Tests if user_client's owned_restaurants returns the exact list
    def test_owned_restaurants_list_correct_list(self):
        msg = "user_client's owned restaurants list does not work accordingly"
        restaurant_ids = ["B6", "SB", "N16", "PDC", "ST"]

        for restaurant_id in restaurant_ids:
            self.assertTrue(restaurant_id in self.user2.owned_restaurants_list, msg)

    #Tests distances_dictionary
    def test_user_dict(self):
        msg = "user distance dict not generated correctly"
        self.assertEqual(self.user.distances_dict, {'ALC': 1.6, 'JK': 0.9, 'KC': 0.9, 'OnF': 1.5, 'BE': 8.1, 'CB': 1.8, 'HBS': 1.1, 'TG': 1.6, 'FM': 1.6, 'ST': 1.8, 'PDC': 0.7, 'N16': 0.6, 'SB': 1.2, 'B6': 3.6, 'GL': 1.2}, msg)


class RestaurantModelTests(TestCase):
    def setUp(self):
        populate()

        self.restaurant = Restaurant.objects.get(name="Alchemilla")

    #Tests Restaurant's __str__ method
    def test_restaurant_str(self):
        msg = "restaurant's string representation does not work accordingly"

        self.assertEqual(str(self.restaurant), "ALC", msg)

    # #Tests if Restaurant's map_link property returns the correct link
    # def test_restaurant_map_link(self):
    #     msg = "restaurant's map link does not work accordingly."
    #
    #     self.assertEqual(self.restaurant.map_link, "1126+Argyle+Street+Glasgow", msg)

    #Tests if Restaurant's rating property computes the rating correctly.
    def test_restaurant_rating(self):
        msg = "restaurant's rating method does not work accordingly."

        self.assertEqual(self.restaurant.rating, 4.29, msg)


