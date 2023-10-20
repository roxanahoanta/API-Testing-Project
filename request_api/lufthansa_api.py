import requests
from dotenv import load_dotenv
import os


class LufthansaApi:
    load_dotenv()

    _CLIENT_KEY = os.getenv("KEY")
    _CLIENT_SECRET = os.getenv("SECRET")
    _BASE_URL = "https://api.lufthansa.com/v1"
    _ACCESS_TOKEN_ENDPOINT = "/oauth/token"
    _FLIGHT_SCHEDULES_ENDPOINT = "/flight-schedules/flightschedules/passenger"
    _REFERENCED_DATA_ENDPOINT = "/mds-references"
    _COUNTRIES_ENDPOINT = "/countries"
    _CITIES_ENDPOINT = "/cities"
    _AIRPORTS_ENDPOINT = "/airports"
    _NEAREST_AIRPORTS_ENDPOINT = "/nearest"
    _OFFERS_ENDPOINT = "/offers"
    _SEATMAPS_ENDPOINT = "/seatmaps"
    _LOUNGES_ENDPOINT = "/lounges"

    def get_access_token(self):
        URL = self._BASE_URL + self._ACCESS_TOKEN_ENDPOINT

        payload = f'grant_type=client_credentials&client_id={self._CLIENT_KEY}&client_secret={self._CLIENT_SECRET}'

        headers_type = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        return requests.post(URL, headers=headers_type, data=payload)

    def get_flight_schedules_passengers(self, access_token, airlines, startDate, endDate, daysOfOperation, timeMode,
                                        flightNumberRanges=None, origin=None, destination=None, aircraftTypes=None):
        URL = self._BASE_URL + self._FLIGHT_SCHEDULES_ENDPOINT

        headers_token = {
            'Authorization': f'Bearer {access_token}'
        }

        parameters = {
            'airlines': airlines,
            'startDate': startDate,
            'endDate': endDate,
            'daysOfOperation': daysOfOperation,
            'timeMode': timeMode,
            'flightNumberRanges': flightNumberRanges,
            'origin': origin,
            'destination': destination,
            'aircraftTypes': aircraftTypes
        }

        return requests.get(URL, headers=headers_token, params=parameters)

    def get_referenced_route(self):
        return self._BASE_URL + self._REFERENCED_DATA_ENDPOINT

    def get_countries_route(self):
        return self.get_referenced_route() + self._COUNTRIES_ENDPOINT

    def get_cities_route(self):
        return self.get_referenced_route() + self._CITIES_ENDPOINT

    def get_airports_route(self):
        return self.get_referenced_route() + self._AIRPORTS_ENDPOINT

    def get_offers_route(self):
        return self._BASE_URL + self._OFFERS_ENDPOINT

    def get_countries(self, access_token, limit=None, offset=None):
        URL = self.get_countries_route()

        headers_token = {
            'Authorization': f'Bearer {access_token}'
        }

        parameters = {
            'limit': limit,
            'offset': offset
        }

        return requests.get(URL, headers=headers_token, params=parameters)

    def get_countries_by_countryCode(self, access_token, countryCode, lang=None):
        URL = self.get_countries_route() + f"/{countryCode}"

        headers_token = {
            'Authorization': f'Bearer {access_token}'
        }

        parameters = {
            'lang': lang
        }

        return requests.get(URL, headers=headers_token, params=parameters)

    def get_cities(self, access_token, limit=None, offset=None):
        URL = self.get_cities_route()
        headers_token = {
            'Authorization': f'Bearer {access_token}'
        }

        parameters = {
            'limit': limit,
            'offset': offset
        }

        return requests.get(URL, headers=headers_token, params=parameters)

    def get_cities_by_cityCode(self, access_token, cityCode, lang=None):
        URL = self.get_cities_route() + f"/{cityCode}"

        headers_token = {
            'Authorization': f'Bearer {access_token}'
        }

        parameters = {
            'lang': lang
        }

        return requests.get(URL, headers=headers_token, params=parameters)

    def get_airports(self, access_token, limit=None, offset=None, LHoperated=None):
        URL = self.get_airports_route()
        headers_token = {
            'Authorization': f'Bearer {access_token}'
        }

        parameters = {
            'limit': limit,
            'offset': offset,
            'LHoperated': LHoperated  # If set to 1, only locations with flights operated by Lufthansa will be returned.
        }

        return requests.get(URL, headers=headers_token, params=parameters)

    def get_airports_by_airportCode(self, access_token, airportCode, lang=None):
        URL = self.get_airports_route() + f"/{airportCode}"

        headers_token = {
            'Authorization': f'Bearer {access_token}'
        }

        parameters = {
            'lang': lang
        }

        return requests.get(URL, headers=headers_token, params=parameters)

    def get_airports_nearest(self, access_token, latitude, longitude, lang=None):
        URL = self._BASE_URL + '/references' + self._AIRPORTS_ENDPOINT + self._NEAREST_AIRPORTS_ENDPOINT + \
              f'/{latitude},{longitude}'

        headers_token = {
            'Authorization': f'Bearer {access_token}'
        }

        parameters = {
            'lang': lang
        }

        return requests.get(URL, headers=headers_token, params=parameters)

    def get_seat_maps(self, access_token, flightNumber, origin, destination, departureDate, cabinClass):
        URL = self.get_offers_route() + self._SEATMAPS_ENDPOINT + \
              f"/{flightNumber}/{origin}/{destination}/{departureDate}/{cabinClass}"

        headers_token = {
            'Authorization': f'Bearer {access_token}'
        }

        return requests.get(URL, headers=headers_token)

    def get_lounges(self, access_token, code, cabinClass="" , tierCode=""):
        URL = self.get_offers_route() + self._LOUNGES_ENDPOINT + f'/{code}'

        # code = The IATA airport code or city code
        def results(status, data):
            valid = {0, 1, 99}
            if status not in valid:
                raise ValueError("results: status must be one of %r." % valid)

        headers_token = {
            'Authorization': f'Bearer {access_token}'
        }

        parameters = {
            'cabinClass': cabinClass,
            'tierCode' : tierCode
        }

        return requests.get(URL, headers=headers_token, params=parameters)
