import requests
from .models import Location
from django.conf import settings


def fetch_coordinates_from_yandex(address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": settings.YANDEX_APIKEY,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None, None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_or_create_location(address):
    location, created = Location.objects.get_or_create(address=address)
    if created or not location.latitude or not location.longitude:
        lat, lon = fetch_coordinates_from_yandex(address)
        if lat is not None and lon is not None:
            location.latitude = lat
            location.longitude = lon
            location.save()
    return location