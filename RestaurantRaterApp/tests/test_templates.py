from django.test import TestCase, Client

from django.urls import reverse
from populate_database import populate_test

class TestTemplates(TestCase):

    def setUp(self):
        populate_test()
        self.client = Client()
        # home
        self.home = reverse("RestaurantRaterApp:home")
        # Show restaurant
        self.show_restaurant = reverse("RestaurantRaterApp:show_restaurant", args=["ALC"])
        # Three version of ratings
        self.explore_rating = reverse("RestaurantRaterApp:explore", args=["rating"])
        self.explore_distance = reverse("RestaurantRaterApp:explore", args=["distance"])
        self.explore_alphabetical = reverse("RestaurantRaterApp:explore", args=["alphabetical"])
        # Favourites
        self.favourites_rating = reverse("RestaurantRaterApp:favourites", args=["rating"])
        self.favourites_distance = reverse("RestaurantRaterApp:favourites", args=["distance"])
        self.favourites_alphabetical = reverse("RestaurantRaterApp:favourites", args=["alphabetical"])
        # Review
        self.review = reverse("RestaurantRaterApp:review", args=["ALC"])
        # Add Restaurant
        # self.add = reverse("RestaurantRaterApp:")
        # Sign-Up
        self.signup = reverse("RestaurantRaterApp:signup")
        # Login Page
        self.login = reverse("RestaurantRaterApp:login")
        # Logout
        self.logout = reverse("RestaurantRaterApp:logout")
        # Reverse Fav
        self.reverse_fav = reverse("RestaurantRaterApp:reverse_fav", args=["ALC"])
        # Add restaurant
        self.addRestaurant = reverse("RestaurantRaterApp:add_restaurant")
        # Profile Page
        self.profile = reverse("RestaurantRaterApp:profile")
        self.delete = reverse('RestaurantRaterApp:delete_profile')
        self.delete_confirm = reverse("RestaurantRaterApp:delete_user")

    def test_home(self):
        response = self.client.get(self.home)

        # Template Asserts
        self.assertTemplateUsed(response, "RestaurantRaterApp/home.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/table.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/stars.html")
        self.assertContains(response, "Check out the Restaurant Rater top ten!")
