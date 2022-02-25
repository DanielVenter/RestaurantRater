from django.contrib import admin
from rango.models import user_client, Restaurant


class user_client_Admin(admin.ModelAdmin):
    list_display = (
        "username", "street_number", "street", "city", "rated_restaurants", "password", "email",
        "name", "surname", "owner_status")


class restaurant_admin(admin.ModelAdmin):
    list_display = ("name", "street_number", "street", "city", "description", "restaurant_id", "comments")


admin.site.register(user_client, user_client_Admin)
admin.site.register(Restaurant, restaurant_admin)

# Register your models here.
