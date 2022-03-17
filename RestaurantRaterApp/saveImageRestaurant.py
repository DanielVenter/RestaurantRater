import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RestaurantRater.settings')

import django

django.setup()
from RestaurantRater import settings
from RestaurantRaterApp.models import Restaurant
from django.core.files import File


def save_images(name):
    files = os.listdir(settings.MEDIA_DIR)
    images = [f for f in files if os.path.isfile(os.path.join(settings.MEDIA_DIR, f))]
    r = Restaurant.objects.get(name=name)
    r.img1.save(os.path.join(name, "img1.jpg"),
                File(open(os.path.join(settings.MEDIA_DIR, images[0]), "rb")))
    r.img2.save(os.path.join(name, "img2.jpg"),
                File(open(os.path.join(settings.MEDIA_DIR, images[1]), "rb")))
    r.img3.save(os.path.join(name, "img3.jpg"),
                File(open(os.path.join(settings.MEDIA_DIR, images[2]), "rb")))
    r.save()
    for image in images:
        os.remove(os.path.join(settings.MEDIA_DIR, image))
