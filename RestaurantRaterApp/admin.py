from django.contrib import admin
from RestaurantRaterApp.models import user_client, Restaurant


class user_client_Admin(admin.ModelAdmin):
    list_display = (
        "user", "name", "surname", "street_number", "street", "city", "rated_restaurants", "owner_status")


class restaurant_admin(admin.ModelAdmin):
    list_display = ("name", "street_number", "street", "city", "description", "restaurant_id", "comments")


admin.site.register(user_client, user_client_Admin)
admin.site.register(Restaurant, restaurant_admin)

# Register your models here.
