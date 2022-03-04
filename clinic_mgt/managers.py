from django.db.models import Manager
import requests
from skote.settings import GEOAPIFY_API_KEY


# class ClinicManager(Manager):
#     def verify(self):
#         self.verified = True
#         return self.verified
#     def make_available(self):
#         self.available_to_work = True
#         return 

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

        geo_data = {'latitude':latitude, 'longitude':longitude}
        return geo_data

