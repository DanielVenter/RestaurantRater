from django.urls import path
from RestaurantRaterApp import views

app_name = 'RestaurantRaterApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/<slug:sort>/', views.explore, name='explore'),
    path('favourites/<slug:sort>/', views.favourites, name='favourites'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('<slug:restaurant_id>/reverse_fav/', views.reverse_favourite_status, name='reverse_fav'),
    path('<slug:restaurant_id>/review/', views.add_review, name='review'),
    path('profile/add_restaurant/', views.add_restaurant, name='add_restaurant'),
    path('<slug:restaurant_id>/', views.show_restaurant, name='show_restaurant'),
]