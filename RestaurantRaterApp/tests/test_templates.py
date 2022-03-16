import reverse as reverse
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

    # Tests restaurant page no user
    def test_show_restaurant_page(self):
        response = self.client.get(self.show_restaurant)

        # Template Assert
        self.assertTemplateUsed(response, "RestaurantRaterApp/restaurant.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")

    def test_explore_rating(self):
        response = self.client.get(self.explore_rating)

        # Template Asserts
        self.assertTemplateUsed(response, "RestaurantRaterApp/explore.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/sort_header.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/stars.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")

    def test_favourites_alpha(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.favourites_alphabetical)

        # Template Asserts
        self.assertTemplateUsed(response, "RestaurantRaterApp/favourites.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/sort_header.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/stars.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/table.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")

    def test_add_review(self):
        print(self.client.login(username="Nicola.H", password="Nicola123"))
        response = self.client.get(self.review)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/add_review.html")

    def test_add_a_restaurant(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.addRestaurant)

        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/add_restaurant.html")

    def test_profile_sign_in(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.profile)

        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/profile.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")

    def test_edit_profile_log_in(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.profile)

        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/profile.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")

    def test_sign_up(self):
        response = self.client.get(self.signup)

        self.assertTemplateUsed(response, "RestaurantRaterApp/signup.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
