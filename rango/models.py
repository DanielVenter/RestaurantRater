from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    street_number = models.PositiveIntegerField()
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    map_link = models.CharField(max_length=256)
    ratings = models.ManyToManyField(User)
    description = models.CharField(max_length=1500)
    img1 = models.ImageField()
    img2 = models.ImageField()
    img3 = models.ImageField()
    ID = models.CharField(primary_key=True)
    comments = models.JSONField()

    @property
    def rating(self):
        total_ratings = []
        for user in self.ratings.all():
            score = user.rated_restaurants[self.name]
            total_ratings.append(score)

        return sum(total_ratings) / len(total_ratings)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.ID)

    def __str__(self):
        return self.ID

class User(models.Model):
    username = models.CharField(primary_key=True)
    liked_restaurants = models.ManyToManyField(Restaurant)
    street_number = models.PositiveIntegerField()
    street = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    rated_restaurants = models.JSONField()
    password = models.CharField(max_length=24)
    email = models.EmailField()
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    owner_status = models.BooleanField(default=False)
    owned_restaurants = models.ManyToManyField(Restaurant)

    @property
    def owned_restaurants_list(self):
        owned_restaurants = []
        for restaurant in User.owned_restaurants.all():
            owned_restaurants.append(restaurant.name)
        return owned_restaurants

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)

    def __str__(self):
        return self.username

# Create your models here.
