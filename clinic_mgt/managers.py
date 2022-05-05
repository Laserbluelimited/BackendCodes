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
        if address is not None:
            try:
                longitude = data['features'][0]['properties']['lon']
                latitude = data['features'][0]['properties']['lat']
                city = data['features'][0]['properties']['city']
                country = data['features'][0]['properties']['country']
                postal_code = data['features'][0]['properties']['postcode']
                geo_data = {'latitude':latitude, 'longitude':longitude, 'city':city, 'country':country, 'postal_code':postal_code}
                return geo_data


            except:
                return None
        else:
            return None

        


