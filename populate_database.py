import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RestaurantRater.settings')
current_dir = os.getcwd()

import django
from django.core.files import File

django.setup()
from rango.models import user_client, Restaurant


def add_restaurant(name, street_number, street, city, description, restaurant_id, comments):
    r = Restaurant.objects.get_or_create(name=name, restaurant_id=restaurant_id, street_number=street_number,
                                         street=street,
                                         city=city, description=description, comments=comments)[0]
    r.generate_map_link()
    images = os.listdir(f"{current_dir}\\PopulateData\\images\\{restaurant_id}")
    r.img1.save(f"{name}\\img1.jpg",
                File(open(f"{current_dir}\\PopulateData\\images\\{restaurant_id}\\{images[0]}", "rb")))
    r.img2.save(f"{name}\\img2.jpg",
                File(open(f"{current_dir}\\PopulateData\\images\\{restaurant_id}\\{images[1]}", "rb")))
    r.img3.save(f"{name}\\img3.jpg",
                File(open(f"{current_dir}\\PopulateData\\images\\{restaurant_id}\\{images[2]}", "rb")))
    r.save()

    return r


def add_user(username, street_number, street, city, liked_restaurants, rated_restaurants, password, email, name,
             surname,
             owner_status=False, owned_restaurants=[]):
    u = user_client.objects.get_or_create(username=username, street_number=street_number, street=street, city=city,
                                          rated_restaurants=rated_restaurants, password=password, email=email,
                                          name=name, surname=surname, owner_status=owner_status)[0]
    u.save()

    # Adds ratings
    for restaurant in rated_restaurants.keys():
        rates(name, restaurant)

    # Adds liked restaurants
    for restaurant in liked_restaurants:
        likes(name, restaurant)

    # Adds Owner's Restaurants
    if owner_status:
        for restaurant in owned_restaurants:
            owns(name, restaurant)

    return u


def rates(user, restaurant):
    user_obj = user_client.objects.get(name=user)
    restaurant_obj = Restaurant.objects.get(restaurant_id=restaurant)
    user_obj.rates.add(restaurant_obj)
    restaurant_obj.ratings.append(user_obj.rated_restaurants[restaurant_obj.restaurant_id])


def owns(user, restaurant):
    user_obj = user_client.objects.get(name=user)
    restaurant_obj = Restaurant.objects.get(restaurant_id=restaurant)
    user_obj.owned_restaurants.add(restaurant_obj)


def likes(user, restaurant):
    user_obj = user_client.objects.get(name=user)
    restaurant_obj = Restaurant.objects.get(restaurant_id=restaurant)
    user_obj.liked_restaurants.add(restaurant_obj)


def populate():
    restaurant_data = [
        # Alchemilla - 1
        {"name": "Alchemilla",
         "street_number": 1126,
         "street": "Argyle Street",
         "city": "Glasgow",
         "description": "Seasonal Mediterranean plates and natural wine.",
         "id": "ALC",
         "comments": {
             "Mark.E": """The restaurant is a cute little intimate location in the interesting area of 
             finnieston. The lighting, ambiance and staff were great and serve the restaurant 
             well. """,
             "Matt.W": """Out-of-the-ordinary small plates. Tasty food and friendly service in a hip 
            setting. Plenty of dishes to choose from. A couple of items on the menu may seem shocking at 
            first. You will be rewarded for being adventurous. """,
             "Danny.M": """Service is wonderful, and the ingredients were fresh and nicely presented, and there is a 
             lot of attention going into the dishes, but it's just not my cup of tea as I found the flavours really 
             bland. Portions are also small, so keep that in mind. I wouldn't come back for the food, but it's worth 
             checking out for yourself """

         }
         },
        # Julie's Kopitiam - 2
        {"name": "Julie's Kopitiam",
         "street_number": 556,
         "street": "Dumbarton Road",
         "city": "Glasgow",
         "description": "Comfort food done right",
         "id": "JK",
         "comments": {
             "Thom.O": """I've enjoyed eating here in the past but £40 for rice, an egg, a chicken leg,
            some cucumber and 3 chickpea fritters is excessive. There is just no attempt to compete at all with the
            great curry houses et al of Glasgow.""",
             "Andy.P": """Fantastic, food was authentic in flavour. The small restaurant has a great vibe
            and the staff were friendly. Good prices. What a gem of a place.""",
             "Danny.M": """Have had some good meals from here but also some pretty disappointing ones. Takeaway this
            evening was overpriced, small in proportion and a let-down across the board. You would hope for more
            consistency. """
         }
         },
        # Kimchi Cult - 3
        {"name": "Kimchi Cult",
         "street_number": 14,
         "street": "Chancellor St",
         "city": "Glasgow",
         "description": "Korean-style fast food in Glasgow’s West End.",
         "id": "KC",
         "comments": {"Nicola.H": """My wife and I tried this tonight after hearing good things and got the Korean 
         Chicken burger, bibimbap and tofu. The food was generally tasty their crispy chicken and sauce was good!""",
                      "Michael.G": """Working in Glasgow, went 3 times in a week. What more can I say. Outstanding""",
                      "Andy.P": """Portion sizes are much smaller now - it is a depressing story for many such 
                        places. Two months ago, their portions were generous and now they are absolutely the 
                        opposite- I won’t be back """
                      }
         },
        # Ox and Finch - 4
        {"name": "Ox and Finch",
         "street_number": 920,
         "street": "Sauchiehall Street",
         "city": "Glasgow",
         "description": "The small plates trend is done very well at this slick Sauchiehall Street restaurant.",
         "id": "OnF",
         "comments": {"Michael.G": """The food served at Ox and Finch, Glasgow is immensely delicious, of the right 
         portion and reasonably priced. You must not give amiss to this place. The service is just superb and there 
         is a variety of meat, vegetables to choose from. You will surely enjoy your meal as I did.""",
                      "Andy.P": """I just love this place and visit on every occasion I'm in Glasgow. The food and 
                      wines are 1st class foods done extremely well. I've been going here for 6+years and I have 
                      never once felt disappointed. Staff and venue are great,will help you with any diet query,
                      same goes for the wines for matching foods."""}
         },
        # Bilson Eleven - 5
        {"name": "Bilson Eleven",
         "street_number": 10,
         "street": "Annfield Place",
         "city": "Glasgow",
         "description": "A five- or even eight-course fine-dining odyssey.",
         "id": "BE",
         "comments": {"Thom.O": """What an unbelievable night that was last night at this restaurant. The food, 
         the service and the wine was absolutely sublime. Just an absolutely unbelievable experience and I certainly 
         would recommend this place to anyone who loves their wine and their fine dining experiences.""",
                      "Michael.G": """Our favourite restaurant in Glasgow . Thank you Nick for a absolute creative 
                      menu visually , sensory & fabulously tasting. Mark,  your front of house was all that we come 
                      to expect, informative, interesting and totally  engrossed in your knowledge of the wines & the 
                      menu, thanks gents"""}
         },
        # Cail Bruich - 6
        {"name": "Cail Bruich",
         "street_number": 725,
         "street": "great Western",
         "city": "Glasgow",
         "description": "Très bon Franco-Scottish cooking.",
         "id": "CB",
         "comments": {"Jeremy.S": """This was our first visit to Cail Bruich. Food and service was excellent, 
         what you'd expect from a Michelin star restaurant. Staff are very knowledgeable about the dishes they serve. 
         We had the chefs tasting menu and was great. Very disappointed by the manner in which a dessert was served, 
         far from Michelin standard or any acceptable standard. This was dealt with at the time with a manager.""",
                      "Matt.W": """Came here for my birthday. I had the tasting menu with wines to match. The wines 
                      did not pair well with the food at all and were particularly expensive and very small measures 
                      (£72 for four very small glasses). You could drive home from this meal without being over the 
                      limit. I've eaten in some wonderful Michelin Starred restaurants and some great AA Rosette 
                      places. This is neither. The restaurant was cold when I visited and the champagne was the worst 
                      I have ever had anywhere. I don't often leave bad reviews but this was a meal for two that cost 
                      close to £500 and wasn't worth it at all. I've spent more in other places but always felt that 
                      I got value for money. I wouldn't go back again."""}
         },
        # Hanoi Bike Shop -7
        {"name": "The Hanoi Bike Shop",
         "street_number": 8,
         "street": "Ruthven Ln",
         "city": "Glasgow",
         "description": "A fresh, casual, canteen-style Vietnamese restaurant.",
         "id": "HBS",
         "comments": {"Matt.W": """We arrived at the Hanoi Bike Shop with much anticipation, joined by our Vietnamese 
         friend. The decor is superb, beautifully decorated. Ordered the spring rolls - delish, followed by a beef 
         pho, average, and my wife got the red duck curry - excellent. I asked for a Vietnamese iced coffee with 
         condensed milk and got a classic iced coffee - disappointed. Our food arrived quickly and the service was 
         good.""",
                      "Mark.E": """Nice cosy interior with an upstairs seating. The shop is easy to find thanks to 
                      the bright signs. The decor of the shop is very nicely done. However the food is quite 
                      disappointing, from an Asian’s point of view. The pho was very disappointing, the portion was 
                      big and all but the taste and correct pho noodles was not satisfactory. They have a lot of side 
                      dishes to eat with their drinks, maybe it’s better for it’s drinks instead of a dinner."""}
         },
        # The Gannet - 8
        {"name": "The Gannet",
         "street_number": 1155,
         "street": "Argyle Street",
         "city": "Glasgow",
         "description": "A slice of Brooklyn-esque cool on the Finnieston ‘strip’.",
         "id": "TG",
         "comments": {}
         },
        # The Finnieston - 9
        {"name": "The Finnieston",
         "street_number": 1125,
         "street": "Argyle Street",
         "city": "Glasgow",
         "description": "Proudly sourced Scottish seafood and gins at a suitably rustic Argyle Street location.",
         "id": "FM",
         "comments": {}
         },
        # Stravaigin - 10
        {"name": "Stravaigin",
         "street_number": 28,
         "street": "Gibson Street",
         "city": "Glasgow",
         "description": "Pub grub staples done very well at a hip West End restaurant.",
         "id": "ST",
         "comments": {}
         },
        # The Patric Duck Club - 11
        {"name": "Patrick Duck Club",
         "street_number": 27,
         "street": "Hyndland Street",
         "city": "Glasgow",
         "description": "A quirky diner proving you can cook duck in A LOT of different ways.",
         "id": "PDC",
         "comments": {}
         },
        # Number 16 - 12
        {"name": "Number 16",
         "street_number": 16,
         "street": "Byres Road",
         "city": "Glasgow",
         "description": "A Euro-bistro in a Byres Road bolthole.",
         "id": "N16",
         "comments": {}
         },
        # Spanish Butcher - 13
        {"name": "Spanish Butcher",
         "street_number": 1055,
         "street": "Sauchiehall Street",
         "city": "Glasgow",
         "description": "Premium Spanish meat served in New York loft-style interiors.",
         "id": "SB",
         "comments": {}
         },
        # Beat 6 - 14
        {"name": "Beat 6",
         "street_number": 10,
         "street": "Whitehall Street",
         "city": "Glasgow",
         "description": """A new venture from the team behind Six by Nico, which donates 100% of its profits to the "
                        Beatson Cancer Charity.""",
         "id": "B6",
         "comments": {}
         },
        # Glorisa -15
        {"name": "Glorisa",
         "street_number": 1321,
         "street": "Argyle Street",
         "city": "Glasgow",
         "description": "For fresh Mediterranean flavours from the chef who brought us Alchemilla.",
         "id": "GL",
         "comments": {}
         },

    ]

    user_data = [
        # Mark Edwards
        {"username": "Mark.E",
         "street_number": 21,
         "street": "Beith Street",
         "city": "Glasgow",
         "liked_restaurants": ["ALC", "SB", "B6"],
         "rated_restaurants": {"ALC": 4, "JK": 2, "ST": 3, "PDC": 2, "N16": 1, "SB": 4, "B6": 5, "GL": 3, "CB": 1,
                               "FM": 2, "TG": 3, "HBS": 1},
         "password": "Mark123",
         "email": "mark@gmail.com",
         "name": "Mark",
         "surname": "Edwards",
         "owner_status": False,
         "owned_restaurants": []
         },
        # Matthew Wainwright
        {"username": "Matt.W",
         "street_number": 164,
         "street": "Buchanan St",
         "city": "Glasgow",
         "liked_restaurants": ["ALC", "JK", "HBS"],
         "rated_restaurants": {"ALC": 5, "JK": 5, "KC": 3, "OnF": 1, "SB": 2, "B6": 1, "GL": 1, "CB": 2, "FM": 2,
                               "TG": 3, "HBS": 4},
         "password": "Matt123",
         "email": "matt@gmail.com",
         "name": "Matthew",
         "surname": "Wainwright",
         "owner_status": False,
         "owned_restaurants": []
         },
        # Thomas Oldman
        {"username": "Thom.O",
         "street_number": 161,
         "street": "Duke St",
         "city": "Glasgow",
         "liked_restaurants": ["ALC", "PDC", "B6", "GL"],
         "rated_restaurants": {"ALC": 4, "JK": 3, "BE": 5, "ST": 3, "PDC": 4, "N16": 2, "SB": 1, "B6": 4, "GL": 5,
                               "TG": 2, "HBS": 3},
         "password": "Thom123",
         "email": "thom@gmail.com",
         "name": "Thomas",
         "surname": "Oldman",
         "owner_status": False,
         "owned_restaurants": []
         },
        # Michael Gunning
        {"username": "Michael.G",
         "street_number": 477,
         "street": "Duke St",
         "city": "Glasgow",
         "liked_restaurants": ["ALC"],
         "rated_restaurants": {"ALC": 4, "JK": 2, "KC": 4, "OnF": 5, "BE": 4, "ST": 2, "PDC": 3},
         "password": "Matt123",
         "email": "matt@gmail.com",
         "name": "Michael",
         "surname": "Gunning",
         "owner_status": False,
         "owned_restaurants": []
         },
        # Andy Peterson
        {"username": "Andy.P",
         "street_number": 394,
         "street": "Great Western Rd",
         "city": "Glasgow",
         "liked_restaurants": ["FM"],
         "rated_restaurants": {"KC": 3, "OnF": 5, "BE": 4, "ST": 2, "PDC": 4, "CB": 3, "FM": 2, "TG": 1, "HBS": 2},
         "password": "Andy123",
         "email": "andy@gmail.com",
         "name": "Andy",
         "surname": "Peterson",
         "owner_status": False,
         "owned_restaurants": []
         },
        # Rose Street
        {"username": "Rose.S",
         "street_number": 8,
         "street": "Cresswell Ln",
         "city": "Glasgow",
         "liked_restaurants": ["ALC", "N16", "B6", "FM"],
         "rated_restaurants": {"ALC": 4, "JK": 4, "ST": 3, "PDC": 2, "N16": 4, "SB": 3, "B6": 4, "GL": 2, "FM": 4,
                               "TG": 3, "HBS": 2},
         "password": "Rose123",
         "email": "rose@gmail.com",
         "name": "Rose",
         "surname": "Street",
         "owner_status": False,
         "owned_restaurants": []
         },
        # Jeremy Stevenson
        {"username": "Jeremy.S",
         "street_number": 1620,
         "street": "Great Western Rd",
         "city": "Glasgow",
         "liked_restaurants": ["SB"],
         "rated_restaurants": {"ST": 2, "PDC": 4, "N16": 2, "SB": 5, "B6": 2, "GL": 1, "CB": 4, "FM": 3, "HBS": 2},
         "password": "Jem123",
         "email": "jeremy@gmail.com",
         "name": "Jeremy",
         "surname": "Stevenson",
         "owner_status": False,
         "owned_restaurants": []
         },
        # Jeff Dalton
        {"username": "Jeff.D",
         "street_number": 108,
         "street": "Queen Margaret Dr",
         "city": "Glasgow",
         "liked_restaurants": ["ALC", "JK", "B6", "GL", "FM"],
         "rated_restaurants": {"ALC": 5, "JK": 4, "KC": 3, "OnF": 1, "ST": 3, "PDC": 2, "B6": 5, "GL": 4, "CB": 3,
                               "FM": 4, "TG": 3, "HBS": 3},
         "password": "Jeff123",
         "email": "jeff@gmail.com",
         "name": "Jeff",
         "surname": "Dalton",
         "owner_status": False,
         "owned_restaurants": []
         },
        # Colin McNair - Owner
        {"username": "Colin",
         "street_number": 1,
         "street": "Cathcard Rd",
         "city": "Glasgow",
         "liked_restaurants": ["PDC", "GL"],
         "rated_restaurants": {"PDC": 3, "N16": 3, "SB": 3, "B6": 2, "GL": 5},
         "password": "Colin123",
         "email": "colin@gmail.com",
         "name": "Colin",
         "surname": "McNair",
         "owner_status": True,
         "owned_restaurants": ["ALC", "JK", "KC", "OnF", "BE"]
         },
        # Nicola Hamill - Owner
        {"username": "Nicola.H",
         "street_number": 530,
         "street": "Victoria Rd",
         "city": "Glasgow",
         "liked_restaurants": ["ALC"],
         "rated_restaurants": {"ALC": 4, "JK": 3, "KC": 3, "HBS": 2},
         "password": "Nichola123",
         "email": "nichola@gmail.com",
         "name": "Nicola",
         "surname": "Hamill",
         "owner_status": True,
         "owned_restaurants": ["ST", "PDC", "N16", "SB", "B6"]
         },
        # Danny Macpherson - Owner
        {"username": "Danny.M",
         "street_number": 316,
         "street": "Calder St",
         "city": "Glasgow",
         "liked_restaurants": ["ST", "SB", "GL"],
         "rated_restaurants": {"ST": 4, "PDC": 3, "N16": 3, "SB": 4, "B6": 3, "GL": 5},
         "password": "Danny123",
         "email": "danny@gmail.com",
         "name": "Danny",
         "surname": "Macpherson",
         "owner_status": True,
         "owned_restaurants": ["GL", "CB", "FM", "TG", "HBS"]

         }]

    for user in user_data:
        add_user(user["username"], user["street_number"], user["street"], user["city"], user["liked_restaurants"],
                 user["rated_restaurants"],
                 user["password"], user["email"], user["name"], user["surname"], user["owner_status"],
                 user["owned_restaurants"])

    for restaurant in restaurant_data:
        add_restaurant(restaurant["name"], restaurant["street_number"], restaurant["street"], restaurant["city"],
                       restaurant["description"], restaurant["id"], restaurant["comments"])


if __name__ == "__main__":
    print("Starting Rango population script")
    populate()
    for u in user_client.objects.all():
        print(f"Created user {u}")
    for r in Restaurant.objects.all():
        print(f"Created restaurant {r}")
    print("Population finished")
