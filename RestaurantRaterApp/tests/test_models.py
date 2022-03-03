from django.test import TestCase
from RestaurantRaterApp.models import user_client, Restaurant
from populate_database import populate

class UserModelTests(TestCase):
    def setUp(self):
        populate()
        self.user = user_client.objects.get(name="Mark")
        self.user2 = user_client.objects.get(name="Nicola")

    def test_user_str(self):
        msg = "user_client's string representation does not work accordingly"

        self.assertEqual(str(self.user), "Mark.E", msg)

    def test_map_link(self):
        msg = "user_client's map link does not work accordingly."

        self.assertEqual(self.user.map_link, "21+Beith+Street+Glasgow", msg)

    def test_owned_restaurants_list_len(self):
        msg = "user_client's owned restaurants list does not work accordingly"

        self.assertEqual(len(self.user.owned_restaurants_list), 0, msg)
        self.assertEqual(len(self.user2.owned_restaurants_list), 5, msg)
    
    def test_owned_restaurants_list_order(self):
        msg = "user_client's owned restaurants list does not work accordingly"

        self.assertEqual(self.user2.owned_restaurants_list[0],"B6" , msg)
    
    def test_owned_restaurants_list_correct_list(self):
        msg = "user_client's owned restaurants list does not work accordingly"
        list = ["B6", "SB", "N16", "PDC", "ST"] 

        for elt in list:
            self.assertTrue(elt in self.user2.owned_restaurants_list, msg)

class RestaurantModelTests(TestCase):
    def setUp(self):
        populate()

        self.restaurant = Restaurant.objects.get(name="Alchemilla")
    
    def test_restaurant_str(self):
        msg = "restaurant's string representation does not work accordingly"

        self.assertEqual(str(self.restaurant), "ALC", msg)

    def test_restaurant_map_link(self):
        msg = "restaurant's map link does not work accordingly."

        self.assertEqual(self.restaurant.map_link, "1126+Argyle+Street+Glasgow",msg)
    
    def test_restaurant_rating(self):
        msg = "restaurant's rating method does not work accordingly."

        self.assertEqual(self.restaurant.rating, 4.29, msg)