import reverse as reverse
from django.test import TestCase, Client

from django.urls import reverse
from populate_database import populate_test
from RestaurantRaterApp.models import Restaurant, user_client
from RestaurantRaterApp.forms import UserForm, SignUpForm
from django.contrib.auth.models import User
from RestaurantRaterApp.forms import UserForm, SignUpForm, EditUserForm, RestaurantForm, ReviewForm, EditSignUpForm


class TestViews(TestCase):

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

    # Tests home page without user
    def test_home_logout(self):
        response = self.client.get(self.home)

        # Content Asserts
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Check out the Restaurant Rater top ten!")
        self.assertEqual(2, len(response.context["restaurants_list"]))
        self.assertEqual(0, len(response.context["favourites"]))

        # Template Asserts
        self.assertTemplateUsed(response, "RestaurantRaterApp/home.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/table.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/stars.html")

    def test_home_login(self):
        self.client.login(username="Mark.E", password="Mark123")
        response = self.client.get(self.home)

        # Content Assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Check out the Restaurant Rater top ten!")
        self.assertEqual(2, len(response.context["restaurants_list"]))
        self.assertNotEqual(0, len(response.context["favourites"]))

        # Template Assert
        self.assertTemplateUsed(response, "RestaurantRaterApp/home.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/table.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/stars.html")

    # Tests restaurant page no user
    def test_show_restaurant_logout(self):
        response = self.client.get(self.show_restaurant)

        # Content Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.context["reviews"]))

        # Template Assert
        self.assertTemplateUsed(response, "RestaurantRaterApp/restaurant.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/stars.html")

    # Tests restaurant page with user
    def test_show_restaurant_login(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.home)

        # Content Asserts
        response = self.client.get(self.show_restaurant)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.context["reviews"]))
        self.assertNotEqual(0, len(response.context["favourites"]))

        # Template Asserts
        self.assertTemplateUsed(response, "RestaurantRaterApp/restaurant.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/stars.html")

    # Tests Explore Page No user - here we are focussing on the difference between the sorts
    def test_explore_logout_rating(self):
        response = self.client.get(self.explore_rating)

        # Content Asserts
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Explore the Restaurant Rater records!")
        self.assertEqual(response.context["sort"], "rating")
        self.assertEqual(response.context["restaurants_list"],
                         [Restaurant.objects.get(restaurant_id="KC"), Restaurant.objects.get(restaurant_id="ALC")])
        self.assertEqual(len(response.context["favourites"]), 0)

        # Template Asserts
        self.assertTemplateUsed(response, "RestaurantRaterApp/explore.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/sort_header.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/stars.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")

    # No need to test templates or content just that the list has been correctly modified
    def test_explore_logout_alphabetical(self):
        response = self.client.get(self.explore_alphabetical)

        self.assertEqual(response.context["sort"], "alphabetical")
        self.assertEqual(response.context["restaurants_list"],
                         [Restaurant.objects.get(restaurant_id="ALC"), Restaurant.objects.get(restaurant_id="KC")])

    # No need to test templates or content just that the list has been correctly modified -needs to be updated once
    # distances are implemented
    def test_explore_logout_distance(self):
        response = self.client.get(self.explore_distance)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["sort"], "distance")
        self.assertEqual(response.context["restaurants_list"],
                         [Restaurant.objects.get(restaurant_id="ALC"), Restaurant.objects.get(restaurant_id="KC")])

    # Testing if user's favourites are returned correctly. No need to test rest of page, repeated above.
    def test_explore_login_rating(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.home)

        self.assertEqual(2, len(response.context["favourites"]))

    def test_favourites_logout_alpha(self):
        response = self.client.get(self.favourites_alphabetical)

        # Checks that the page can't be accessed
        self.assertEqual(response.status_code, 302)

    def test_favourites_login_alpha(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.favourites_alphabetical)

        # Content Asserts
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View your favourite restaurants!")
        self.assertEqual(response.context["sort"], "alphabetical")
        self.assertEqual(response.context["restaurants_list"],
                         [Restaurant.objects.get(restaurant_id="ALC"), Restaurant.objects.get(restaurant_id="KC")])

        # Template Asserts
        self.assertTemplateUsed(response, "RestaurantRaterApp/favourites.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/sort_header.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/stars.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/table.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")

    # Checks favourite page when sorted by distance
    def test_favourites_login_distance(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.favourites_alphabetical)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["sort"], "alphabetical")
        self.assertEqual(response.context["restaurants_list"],
                         [Restaurant.objects.get(restaurant_id="ALC"), Restaurant.objects.get(restaurant_id="KC")])

    # Checks favourite page regarding rating
    def test_favourites_login_rating(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.favourites_rating)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["sort"], "rating")
        self.assertEqual(response.context["restaurants_list"],
                         [Restaurant.objects.get(restaurant_id="KC"), Restaurant.objects.get(restaurant_id="ALC"), ])

    # Makes sure Anon users can't add a review
    def test_add_review_logout(self):
        response = self.client.get(self.review)

        self.assertEqual(response.status_code, 302)


    # Can't complete test
    def test_add_review_login(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.review)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "restaurantraterapp/add_review.html")

    def test_add_restaurant_logout(self):
        response = self.client.get(self.addRestaurant)

        self.assertEqual(response.status_code, 302)

    def test_add_restaurant(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.addRestaurant)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "restaurantraterapp/add_restaurant.html")

    def test_profile_logout(self):
        response = self.client.get(self.profile)

        self.assertEqual(response.status_code, 302)

    def test_profile_signin(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.profile)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["account_details"]["Username"], "Nicola.H")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/profile.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")

    def test_edit_profile_logout(self):
        response = self.client.get(self.profile)

        self.assertEqual(response.status_code, 302)

    def test_edit_profile_login(self):
        self.client.login(username="Nicola.H", password="Nicola123")
        response = self.client.get(self.profile)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/profile.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/arrow_or_heart.html")


    def test_signup_good(self):
        response = self.client.get(self.signup)

        # Content Assert
        user_data = {'username': 'testuser', 'password': 'test123', 'email': 'test@test.com'}
        user_form = UserForm(data=user_data)

        user_profile_data = {'name': "test", 'surname': "test", 'city': "glasgow", 'street': "Beith Street",
                             'street_number': 21}
        user_profile_form = SignUpForm(data=user_profile_data)

        self.assertTrue(user_form.is_valid())
        self.assertTrue(user_profile_form.is_valid())

        user_obj = user_form.save()
        user_obj.set_password(user_data["password"])
        user_obj.save()

        user_profile_obj = user_profile_form.save(commit=False)
        user_profile_obj.user = user_obj
        user_profile_obj.save()

        # Three users already exist
        self.assertEqual(len(User.objects.all()), 4)
        self.assertEqual(len(user_client.objects.all()), 4)

        # Template Asserts
        self.assertTemplateUsed(response, "RestaurantRaterApp/signup.html")
        self.assertTemplateUsed(response, "RestaurantRaterApp/base.html")
        self.assertTrue(self.client.login(username='testuser', password='test123'))


    def test_user_login(self):
        user_obj = user_client.objects.get(name="Nicola")

        response = self.client.post(self.login, {"username": user_obj.user.username, "password": "Nicola123"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual("Nicola.H", f"{response.wsgi_request.user}")
        self.assertEqual(response.url, self.home)

    def test_user_logout(self):
        user_obj = user_client.objects.get(name="Nicola")
        self.client.login(username="Nicola.H", password="Nicola123")
        self.assertEqual(user_obj.id, int(self.client.session['_auth_user_id']))

        response = self.client.get(self.logout)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.home)
        self.assertTrue('_auth_user_id' not in self.client.session)


    def test_reverse_favourite_status_remove(self):
        user_obj = user_client.objects.get(name="Nicola")
        self.client.login(username="Nicola.H", password="Nicola123")

        response = self.client.get(self.reverse_fav)

        self.assertTrue(Restaurant.objects.get(restaurant_id="ALC") not in list(user_obj.liked_restaurants.all()))

    def test_reverse_favourite_status_add(self):
        user_obj = user_client.objects.get(name="Colin")
        self.client.login(username="Colin", password="Colin123")

        response = self.client.get(self.reverse_fav)
        print(list(user_obj.liked_restaurants.all()))

        self.assertTrue(Restaurant.objects.get(restaurant_id="ALC") in list(user_obj.liked_restaurants.all()))
