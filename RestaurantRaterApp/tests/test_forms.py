from django.test import TestCase, Client
from django.urls import reverse

from RestaurantRaterApp.models import user_client, Restaurant
from populate_database import populate_test
import os

from RestaurantRaterApp.forms import UserForm, SignUpForm, EditUserForm, RestaurantForm

current_dir = os.getcwd()

class FormTests(TestCase):
    def setUp(self):
        populate_test()
        self.user = user_client.objects.get(name="Mark")
        self.user2 = user_client.objects.get(name="Nicola")

    def test_userForm_good(self):
        form = UserForm(data={"username": "Dan.V", "password": "Daniel123", "email": "dan@gmail.com"})

        self.assertTrue(form.is_valid())

    def test_userForm_bad_username(self):
        form = UserForm(data={"username": "Nicola.H", "password": "Daniel123", "email": "dan@gmail.com"})

        self.assertEqual(form.errors, {'username': ['A user with that username already exists.']})

    def test_userForm_bad_password(self):
        form = UserForm(data={"username": "Dan.V", "password": "", "email": "dan@gmail.com"})

        self.assertEqual(form.errors, {'password': ['This field is required.']})

    def test_userForm_bad_email(self):
        form = UserForm(data={"username": "Dan.V", "password": "Daniel123", "email": "dangmail.com"})

        self.assertEqual(form.errors, {'email': ['Enter a valid email address.']})

    def test_SignUpForm_good(self):
        form = SignUpForm(data={"name": "Daniel", "surname": "Venter", "city": "Glasgow", "street": "Beith Street",
                                "street_number": 21})

        self.assertTrue(form.is_valid())

    def test_SignUpForm_bad_name_surname(self):
        form = SignUpForm(
            data={"name": "", "surname": "", "city": "Glasgow", "street": "Beith Street", "street_number": 21})

        self.assertEqual(form.errors, {'name': ['This field is required.'], 'surname': ['This field is required.']})

    def test_SignUpForm_bad_address(self):
        client = Client()
        client.login(username="Mark.E", password="Mark123")
        response = client.get(reverse("RestaurantRaterApp:add_restaurant"))
        # JS validation done so need to render the page
        form = SignUpForm(
            data={"name": "", "surname": "", "city": "asdfa", "street": "asdasd", "street_number": 21})

        self.assertContains(response, "Address invalid")


    def test_EditUserForm_good(self):
        form = EditUserForm(data={"username": "Dan.V", "email": "dan@gmail.com"})

        self.assertTrue(form.is_valid())

    def test_EditUserForm_bad(self):
        form = EditUserForm(data={"username": "Nicola.H", "email": "dangmail.com"})

        self.assertEqual(form.errors, {'username': ['A user with that username already exists.'],
                                       'email': ['Enter a valid email address.']})

    def test_RestaurantForm_bad(self):
        form = RestaurantForm(
            data={'name': "Cafe", 'street_number': "21", 'street': "Valley Road", 'city': "Johannesburg",
                  'description': "Some basic text here"})
        # Image error and integer error
        self.assertFalse(form.is_valid())

