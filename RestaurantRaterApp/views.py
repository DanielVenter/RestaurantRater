from django.shortcuts import render
from django.http import HttpResponse
from RestaurantRaterApp.forms import UserForm, SignUpForm, EditForm, RestaurantForm, ReviewForm
from RestaurantRaterApp.models import Restaurant, user_client
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm


def home(request):
    restaurants_list = list(Restaurant.objects.all())
    restaurants_list.sort(reverse=True, key=lambda x: x.rating)
    this_user = request.user
    context_dict = {"restaurants_list": restaurants_list[:10],
                    "titlemessage": "Check out the Restaurant Rater top ten!"}
    try:
        this_user = user_client.objects.get(user=this_user)
        favourites = list(this_user.liked_restaurants.all())
        distances = this_user.distances_dict.copy()
        context_dict['favourites'] = favourites
        context_dict['distances'] = distances

    except Exception as e:
        context_dict['favourites'] = []
        context_dict['distances'] = []

    return render(request, 'RestaurantRaterApp/home.html', context=context_dict)


def show_restaurant(request, restaurant_id):
    try:
        this_user = request.user
        this_user = user_client.objects.get(user=this_user)
        favourites = list(this_user.liked_restaurants.all())
    except:
        favourites = []

    context_dict = {}
    try:

        restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)

        context_dict['restaurant'] = restaurant
        context_dict['reviews'] = restaurant.comments
    except Restaurant.DoesNotExist:

        context_dict['restaurant'] = None

    context_dict['favourites'] = favourites
    return render(request, 'RestaurantRaterApp/restaurant.html', context=context_dict)


def explore(request, sort):
    this_user = request.user
    restaurants_list = list(Restaurant.objects.all())
    sort_options = sort_by(restaurants_list, sort, this_user)
    context_dict = {"restaurants_list": restaurants_list,
                    "titlemessage": "Explore the Restaurant Rater records!",
                    "sort": sort,
                    "sort_opts": sort_options}
    try:
        this_user = user_client.objects.get(user=this_user)
        favourites = list(this_user.liked_restaurants.all())
        distances = this_user.distances_dict.copy()
        context_dict['favourites'] = favourites
        context_dict['distances'] = distances
    except:
        context_dict['favourites'] = []
        context_dict['distances'] = []

    return render(request, 'RestaurantRaterApp/explore.html', context=context_dict)


@login_required
def favourites(request, sort):
    this_user = request.user
    this_user = user_client.objects.get(user=this_user)
    distances = this_user.distances_dict.copy()
    favourites = list(this_user.liked_restaurants.all())
    sort_options = sort_by(favourites, sort, request.user)

    context_dict = {"restaurants_list": favourites,
                    "distances": distances,
                    "titlemessage": "View your favourite restaurants!",
                    "sort": sort,
                    "sort_opts": sort_options}
    return render(request, 'RestaurantRaterApp/favourites.html', context=context_dict)


# helper function for explore and favourites views
def sort_by(list, sort, user):
    if sort == "alphabetical":
        list.sort(key=lambda x: x.name)
    elif sort == "distance" and user.is_authenticated:
        user = user_client.objects.get(user=user)
        distances = user.distances_dict.copy()
        my_list = []
        while distances:
            largest = 0
            largest_id = None
            for restaurant_id in distances:
                if distances[restaurant_id] > largest:
                    largest = distances[restaurant_id]
                    largest_id = restaurant_id
            my_list.append(Restaurant.objects.get(restaurant_id=largest_id))
            distances.pop(largest_id)
        list.clear
        my_list.reverse()
        list = my_list
    elif sort == "rating":
        list.sort(reverse=True, key=lambda x: x.rating)
    return ["alphabetical", "distance", "rating"]


@login_required
def add_review(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    except Restaurant.DoesNotExist:
        restaurant = None

    if restaurant is None:
        return redirect('/restaurantraterapp/')
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if restaurant:
                form.save(commit=False)

                return redirect(reverse('restaurantraterapp:show_restaurant', kwargs={'restaurant_id': restaurant_id}))
    else:
        print(form.errors)
    context_dict = {'form': form, 'restaurant': restaurant}
    return render(request, 'restaurantraterapp/add_review.html', context=context_dict)


@login_required
def add_restaurant(request):
    form = RestaurantForm()

    if request.method == 'POST':
        form = RestaurantForm(request.POST)

        if form.is_valid():
            restaurant = form.save(commit=True)
            print(restaurant, restaurant.id)
            request.user.owner_status = True

        return redirect('/restaurantraterapp/')
    else:

        print(form.errors)

    return render(request, 'restaurantraterapp/add_restaurant.html', {'form': form})


@login_required
def profile(request):
    context_dict = {}
    this_user = request.user
    this_user_client = user_client.objects.get(user=this_user)
    context_dict['restaurants_list'] = this_user_client.owned_restaurants_list
    context_dict['favourites'] = list(this_user_client.liked_restaurants.all())

    restaurants = list(Restaurant.objects.all())
    users_comments = {}
    for restaurant in restaurants:
        for com in restaurant.comments:
            if com == this_user.username:
                users_comments[restaurant.name] = restaurant.comments[com]
    context_dict['comments'] = users_comments

    context_dict['account_details'] = {"Username": this_user.username,
                                       "Name": this_user_client.name,
                                       "Surname": this_user_client.surname,
                                       "Email": this_user.email,
                                       "Address": f"{this_user_client.street_number} {this_user_client.street} {this_user_client.city}"}

    return render(request, 'RestaurantRaterApp/profile.html', context=context_dict)


def edit_profile(request):
    if request.method == 'POST':
        edit_form = EditForm(request.POST, instance=request.user)

        if edit_form.is_valid():
            edit_form.save()
            return redirect('RestaurantRaterApp/profile')



        else:

            return redirect('RestaurantRaterApp/edit_profile')
    else:
        edit_form = EditForm()

    context_dict = {'edit_form': edit_form}
    return render(request, 'RestaurantRaterApp/edit_profile.html', context_dict)


def change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(data=request.POST, user=request.user)

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return redirect('restaurantraterapp/profile')

        else:

            return redirect('RestaurantRaterApp/change_password')
    else:
        password_form = PasswordChangeForm(user=request.user)

    context_dict = {'password_form': password_form}
    return render(request, 'RestaurantRaterApp/change_password.html', context_dict)


def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        signup_form = SignUpForm(request.POST)
        if user_form.is_valid() and signup_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            usr_client = signup_form.save(commit=False)
            usr_client.user = user
            usr_client.save()

            usr_client.update_distances_dict()

            registered = True
        else:
            print(user_form.errors, signup_form.errors)
    else:
        user_form = UserForm()
        signup_form = SignUpForm()
    context_dict = {'user_form': user_form,
                    'signup_form': signup_form,
                    'registered': registered,
                    'titlemessage': "Sign up for a Restaurant Rater account!"}
    return render(request, 'RestaurantRaterApp/signup.html', context_dict)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('RestaurantRaterApp:home'))
            else:
                return HttpResponse("Your RestaurantRaterApp account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'RestaurantRaterApp/login.html', {"titlemessage": "Log in to your Restaurant Rater account!"})


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('RestaurantRaterApp:home'))


@login_required
def reverse_favourite_status(request, restaurant_id):
    restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    this_user = request.user
    this_user = user_client.objects.get(user=this_user)
    if restaurant in this_user.liked_restaurants.all():
        this_user.liked_restaurants.remove(restaurant)
    else:
        this_user.liked_restaurants.add(restaurant)
    return redirect(reverse('RestaurantRaterApp:show_restaurant', kwargs={'restaurant_id': restaurant_id}))

@login_required
def del_confirm(request):
    return render(request, 'RestaurantRaterApp/delete_confirmation.html', {"titlemessage": "Do you want to delete your Restaurant Rater account?"})

@login_required
def del_user(request):
    #TODO: delete the user
    return redirect(reverse('RestaurantRaterApp:home'))