from django.db.models import Manager
import requests
from skote.settings import GEOAPIFY_API_KEY


class AddressRequest():

    def get_geodata(self, address):

        parameters = {
            "text":address,
            "apiKey":GEOAPIFY_API_KEY,
        }
        response = requests.get("https://api.geoapify.com/v1/geocode/search", params=parameters)
        data= response.json()
        longitude = data['features'][0]['properties']['lon']
        latitude = data['features'][0]['properties']['lat']
        city = data['features'][0]['properties']['city']
        country = data['features'][0]['properties']['country']

        geo_data = {'latitude':latitude, 'longitude':longitude, 'city':city, 'country':country}
        return geo_data

