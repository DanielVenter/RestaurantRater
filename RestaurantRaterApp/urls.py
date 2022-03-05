from django.urls import path
from RestaurantRaterApp import views

app_name = 'RestaurantRaterApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('favourites/', views.favourites, name='favourites'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('<slug:restaurant_id>/',views.show_restaurant, name='show_restaurant'),
]