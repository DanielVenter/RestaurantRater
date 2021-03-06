from django.shortcuts import render
from django.http import HttpResponse
from RestaurantRaterApp.forms import UserForm, SignUpForm, EditUserForm, RestaurantForm, ReviewForm, EditSignUpForm
from RestaurantRaterApp.models import Restaurant, user_client
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
import googlemaps
from django.contrib.auth.forms import PasswordChangeForm
from RestaurantRaterApp.saveImageRestaurant import save_images


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


@login_required(login_url='RestaurantRaterApp:login')
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
        list.sort(key=lambda x: distances[x.restaurant_id])


    elif sort == "rating":
        list.sort(reverse=True, key=lambda x: x.rating)
    return ["alphabetical", "distance", "rating"]


@login_required(login_url='RestaurantRaterApp:login')
def add_review(request, restaurant_id):
    this_user = request.user
    this_user_client = this_user.user_client
    try:
        restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    except Restaurant.DoesNotExist:
        restaurant = None

    if restaurant is None:
        return redirect('/RestaurantRaterApp/')

    if restaurant.restaurant_id in this_user_client.rated_restaurants.keys() or restaurant in this_user_client.owned_restaurants.all():
        return redirect(reverse('RestaurantRaterApp:show_restaurant', kwargs={'restaurant_id': restaurant_id}))

    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            restaurant.comments[this_user.username] = form.cleaned_data['review']
            restaurant.ratings.append(float(form.cleaned_data["rating"]))
            restaurant.save()
            this_user_client.rated_restaurants[restaurant_id] = float(form.cleaned_data["rating"])
            this_user_client.rates.add(restaurant)
            this_user_client.save()
            return redirect(reverse('RestaurantRaterApp:show_restaurant', kwargs={'restaurant_id': restaurant_id}))
    else:
        print(form.errors)
    context_dict = {'form': form, 'restaurant': restaurant}
    return render(request, 'RestaurantRaterApp/add_review.html', context=context_dict)


@login_required(login_url='RestaurantRaterApp:login')
def add_restaurant(request):
    invalid_name = False
    invalid_address = 0
    form = RestaurantForm()
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():

            if not validate_address(form.cleaned_data["street"], form.cleaned_data["street_number"], form.cleaned_data["city"]):
                invalid_address = 1
                return render(request, 'RestaurantRaterApp/add_restaurant.html', {'form': form, 'invalid_name':invalid_name, 'invalid_address':invalid_address})

            restaurant = form.save()
            save_images(restaurant.name)
            request.user.user_client.owner_status = True
            for usr_client in user_client.objects.all():
                usr_client.update_distances_dict()
            request.user.user_client.owned_restaurants.add(restaurant)
            return redirect('RestaurantRaterApp:profile')
        else:
            invalid_name = True
            if not validate_address(form.cleaned_data["street"], form.cleaned_data["street_number"], form.cleaned_data["city"]):
                invalid_address = 1
                return render(request, 'RestaurantRaterApp/add_restaurant.html', {'form': form, 'invalid_name':invalid_name, 'invalid_address':invalid_address})

    return render(request, 'RestaurantRaterApp/add_restaurant.html', {'form': form, 'invalid_name':invalid_name, 'invalid_address':invalid_address})


@login_required(login_url='RestaurantRaterApp:login')
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


@login_required(login_url='RestaurantRaterApp:login')
def edit_profile(request):
    updated = False
    # Flags for username authenticity and address validation.
    invalid_username = False
    invalid_address = 0
    if request.method == 'POST':
        edit_user_form = EditUserForm(request.POST, instance=request.user)
        edit_signup_form = EditSignUpForm(request.POST)

        if edit_user_form.is_valid() and edit_signup_form.is_valid():

            #If address is not valid, do not submit the form.
            if not validate_address(edit_signup_form.cleaned_data["street"], edit_signup_form.cleaned_data["street_number"], edit_signup_form.cleaned_data["city"]):
                invalid_address = 1
                context_dict = {'edit_user_form': edit_user_form,
                    'edit_signup_form': edit_signup_form,
                    'invalid_username': invalid_username,
                    'invalid_address': invalid_address,
                    'titlemessage': "Sign up for a Restaurant Rater account!",
                    'users': [usr.username for usr in User.objects.all()], }
                return render(request, 'RestaurantRaterApp/edit_profile.html', context_dict)

            #If this point is reached, form was successful
            #Therefore, udpate user profile
            old_address = request.user.user_client.city + request.user.user_client.street + str(
                request.user.user_client.street_number)
            request.user.username = edit_user_form.cleaned_data['username']
            request.user.email = edit_user_form.cleaned_data['email']
            request.user.user_client.name = edit_signup_form.cleaned_data['name']
            request.user.user_client.surname = edit_signup_form.cleaned_data['surname']
            request.user.user_client.street = edit_signup_form.cleaned_data['street']
            request.user.user_client.city = edit_signup_form.cleaned_data['city']
            request.user.user_client.street_number = edit_signup_form.cleaned_data['street_number']
            request.user.save()
            request.user.user_client.save()
            new_address = request.user.user_client.city + request.user.user_client.street + str(
                request.user.user_client.street_number)



            if not ( (old_address == new_address) and len(Restaurant.objects.all()) > 0):
                request.user.user_client.update_distances_dict(new_address=True)

            return redirect(reverse('RestaurantRaterApp:profile'))
        else:
            invalid_username = True
            #Need this extra if because edit_signup_form won't have cleaned_data dictionary.
            if edit_signup_form.is_valid():
                if not validate_address(edit_signup_form.cleaned_data["street"], edit_signup_form.cleaned_data["street_number"], edit_signup_form.cleaned_data["city"]):
                       invalid_address = 1

    else:
        edit_user_form = EditUserForm(instance=request.user)
        edit_signup_form = EditSignUpForm(instance=request.user.user_client)

    context_dict = {'edit_user_form': edit_user_form,
                    'edit_signup_form': edit_signup_form,
                    'titlemessage': "Update your Restaurant Rater account details!",
                    'updated': updated,
                    'invalid_username': invalid_username,
                    'invalid_address': invalid_address,}
    return render(request, 'RestaurantRaterApp/edit_profile.html', context_dict)

def signup(request):
    registered = False

    # Flags for username authenticity and address validation.
    invalid_username = False
    invalid_address = 0

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        signup_form = SignUpForm(request.POST)
        if user_form.is_valid() and signup_form.is_valid():
            user = user_form.save()
            usr_client = signup_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            usr_client.user = user
            usr_client.save()

            #If address is not valid, do not submit the form.
            if not validate_address(signup_form.cleaned_data["street"], signup_form.cleaned_data["street_number"], signup_form.cleaned_data["city"]):
                invalid_address = 1
                user.delete()
                usr_client.delete()

                context_dict = {'user_form': user_form,
                    'signup_form': signup_form,
                    'registered': False,
                    'invalid_username': invalid_username,
                    'invalid_address': invalid_address,
                    'titlemessage': "Sign up for a Restaurant Rater account!",
                    'users': [usr.username for usr in User.objects.all()], }
                return render(request, 'RestaurantRaterApp/signup.html', context_dict)

            # If there are no restaurants on the server then updating the distances matrix will cause error.
            if len(Restaurant.objects.all()) > 0:
                usr_client.update_distances_dict()

            registered = True
        else:
            invalid_username = True
            #Need this extra if because signup_form won't have cleaned_data dictionary.
            if signup_form.is_valid():
                if not validate_address(signup_form.cleaned_data["street"], signup_form.cleaned_data["street_number"], signup_form.cleaned_data["city"]):
                       invalid_address = 1
    else:
        user_form = UserForm()
        signup_form = SignUpForm()
    context_dict = {'user_form': user_form,
                    'signup_form': signup_form,
                    'registered': registered,
                    'invalid_username': invalid_username,
                    'invalid_address': invalid_address,
                    'titlemessage': "Sign up for a Restaurant Rater account!",
                    'users': [usr.username for usr in User.objects.all()], }
    return render(request, 'RestaurantRaterApp/signup.html', context_dict)


def user_login(request):
    invalid = False
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
            return render(request, 'RestaurantRaterApp/login.html',
                          {"titlemessage": "Log in to your Restaurant Rater account!", "invalid": True})
    else:
        return render(request, 'RestaurantRaterApp/login.html',
                      {"titlemessage": "Log in to your Restaurant Rater account!"})


@login_required(login_url='RestaurantRaterApp:login')
def user_logout(request):
    logout(request)
    return redirect(reverse('RestaurantRaterApp:home'))


@login_required(login_url='RestaurantRaterApp:login')
def reverse_favourite_status(request, restaurant_id):
    restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
    this_user = request.user
    this_user = user_client.objects.get(user=this_user)
    if restaurant in this_user.liked_restaurants.all():
        this_user.liked_restaurants.remove(restaurant)
    else:
        this_user.liked_restaurants.add(restaurant)
    return redirect(reverse('RestaurantRaterApp:show_restaurant', kwargs={'restaurant_id': restaurant_id}))


@login_required(login_url='RestaurantRaterApp:login')
def del_confirm(request):
    return render(request, 'RestaurantRaterApp/delete_confirmation.html',
                  {"titlemessage": "Do you want to delete your Restaurant Rater account?"})


@login_required(login_url='RestaurantRaterApp:login')
def del_user(request):
    u = request.user
    u.delete()

    return redirect(reverse('RestaurantRaterApp:home'))

#Method to check address.
def validate_address(street, street_number, city):
     # Using google maps geocode API.
            gmaps_key = googlemaps.Client(key="AIzaSyA5dcV3e9Oe4ZED0UkRRH4P1f4sMG3LSrw")

            # Geocodes the address.
            g = gmaps_key.geocode(
                str(street_number) + " " + street + ", " +
                city)

            # If length is 0 then no address has been matched.
            if len(g) == 0:
                return False

            # If length is greater than 1, then two address-related fields are different valid locations.
            elif len(g) > 1:
                return False

            # If we reached this place, now we check that all the fields (street, city and street number) are correct
            # If not, then we don't submit the form.
            else:
                city_ok = street_ok = street_nr_ok = False
                for x in g[0]['address_components']:
                    if city.lower() in x['long_name'].lower():
                        city_ok = True
                    elif street.lower() in x['long_name'].lower() or street.lower() in x['short_name'].lower():
                        street_ok = True
                    elif str(street_number) == str(x['long_name']):
                        street_nr_ok = True

                if not (city_ok and street_ok and street_nr_ok):
                    return False
            
            return True