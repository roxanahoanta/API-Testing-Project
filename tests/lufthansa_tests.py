import json
import unittest
from request_api.lufthansa_api import LufthansaApi


class LufthansaTests(unittest.TestCase):
    accessToken = ''

    def setUp(self) -> None:
        self.lufthansa = LufthansaApi()
        if self.accessToken == '':
            self.accessToken = self.lufthansa.get_access_token().json()['access_token']

    # """    --------------------------------------POSITIVE TESTING--------------------------------------------------"""

    def test_flight_schedules_passengers(self):
        # check the information of the flights operated by Lufthansa
        # between December 5, 2023, and December 10, 2023, with departures
        # on all days of the week and with a flight number less than 10

        given_airline = "LH"
        given_startDate = "05DEC23"
        given_endDate = "10DEC23"
        given_daysOfOperation = "1234567"
        given_timeMode = "UTC"
        given_flightNumberRanges = "-10"

        response = self.lufthansa.get_flight_schedules_passengers(self.accessToken, given_airline, given_startDate,
                                                                  given_endDate, given_daysOfOperation, given_timeMode,
                                                                  given_flightNumberRanges)

        self.assertEqual(response.status_code, 200, "Status code is not as expected")
        for flight in response.json():
            self.assertEqual(flight["airline"], given_airline,
                             f"The flight information does not belong to the {given_airline} airline")
            self.assertLessEqual(flight["flightNumber"], 10)

    def test_get_countries_by_limit(self):
        # check the list of countries with a limit of 3 elements

        given_limit = 3

        response = self.lufthansa.get_countries(self.accessToken, limit=given_limit)

        self.assertEqual(response.status_code, 200, "Status code is not the same")
        response_length = len(response.json()["CountryResource"]["Countries"]["Country"])
        self.assertEqual(given_limit, response_length, "Response body does not respect given limit")

    def test_get_countries_by_countryCode(self):
        # check the name in Spanish of a country that has the code "DE"

        given_language = "ES"
        given_countryCode = "DE"

        response = self.lufthansa.get_countries_by_countryCode(self.accessToken, given_countryCode, given_language)

        self.assertEqual(response.status_code, 200, "Status code is not the same")
        self.assertEqual(response.json()["CountryResource"]["Countries"]["Country"]["CountryCode"], given_countryCode,
                         "This is not the given countryCode")
        self.assertEqual("Alemania", response.json()["CountryResource"]["Countries"]["Country"]["Names"]["Name"]["$"],
                         f"Country Name for {given_language} language is not correct")

    def test_get_cities(self):
        # check the first element in the list of cities

        response = self.lufthansa.get_cities(self.accessToken)

        self.assertEqual(response.status_code, 200, "Status code is not the same")
        self.assertEqual("AAA", response.json()["CityResource"]["Cities"]["City"][0]["CityCode"],
                         "The first element in the list is not correct")

    def test_get_cities_by_cityCode(self):
        # check a city with "AAM" code

        given_cityCode = "AAM"

        response = self.lufthansa.get_cities_by_cityCode(self.accessToken, given_cityCode)

        self.assertEqual(response.status_code, 200, "Status code is not the same")
        self.assertEqual(given_cityCode, response.json()["CityResource"]["Cities"]["City"]["CityCode"],
                         f"Response does not respect given City code f{given_cityCode}")

    def test_get_airports(self):
        # check the list of airports operated by Lufthansa with a limit of 44 and an offset of 123

        given_limit = 44
        given_offset = 123
        given_LHoperated = 1

        response = self.lufthansa.get_airports(self.accessToken, limit=given_limit, offset=given_offset,
                                               LHoperated=given_LHoperated)

        self.assertEqual(response.status_code, 200, "Status code is not the same")
        for airport in response.json()["AirportResource"]["Airports"]["Airport"]:
            self.assertEqual("Airport", airport["LocationType"], "Object type is not correct")
        response_length = len(response.json()["AirportResource"]["Airports"]["Airport"])
        self.assertEqual(given_limit, response_length, "Response length does not respect the limit")

    def test_get_seat_maps(self):
        # check the seat map of flight number 153 operated by Lufthansa on 2023-12-05, departing from NUE to FRA in
        # Economy class

        given_flightNumber = "LH153"
        given_origin = "NUE"
        given_destination = "FRA"
        given_departureDate = "2023-12-05"
        given_cabinClass = "M"

        response = self.lufthansa.get_seat_maps(self.accessToken, given_flightNumber, given_origin, given_destination,
                                                given_departureDate, given_cabinClass)

        self.assertEqual(response.status_code, 200, "Status code is not the same")
        response_date = \
            response.json()["SeatAvailabilityResource"]["Flights"]["Flight"]["Departure"]["ScheduledTimeLocal"][
                "DateTime"]
        self.assertIn(given_departureDate, response_date, "Departure date does not match the entered value")
        response_exits = response.json()["SeatAvailabilityResource"]["CabinLayout"]
        self.assertIn("ExitRowPosition", response_exits, "Seat map does not have exit seats")


    # """    --------------------------------------NEGATIVE TESTING--------------------------------------------------"""

    def test_get_airports_by_invalid_code(self):
        # check an airport with a wrong code value

        given_airportCode = "invalidCode"

        response = self.lufthansa.get_airports_by_airportCode(self.accessToken, given_airportCode)

        self.assertEqual(response.status_code, 400, "Status code is not the same")
        expected_error = "Invalid airport code (formally incorrect)."
        self.assertIn(expected_error, response.json()["ProcessingErrors"]["ProcessingError"]["Description"],
                      "Error description is not the same")

    def test_get_airports_nearest_by_invalid_parameters(self):
        # check nearest airports with a lower and a boundary value of longitude and latitude from the accepted range

        given_latitude = -108
        given_longitude = -180

        response = self.lufthansa.get_airports_nearest(self.accessToken, given_latitude, given_longitude)
        self.assertEqual(response.status_code, 400, "Status code is not the same")
        expected_error = "Invalid latitude, longitude (formally incorrect)"
        self.assertIn(expected_error, response.json()["ProcessingErrors"]["ProcessingError"]["Description"],
                      "Error description is not the same")

    def test_get_lounges_by_invalid_cabinClass(self):
        # check lounges list from SBZ with integer value for cabin class

        given_code = "SBZ"
        given_cabinClass = 3

        response = self.lufthansa.get_lounges(self.accessToken, given_code, given_cabinClass)
        self.assertEqual(response.status_code, 400, "Status code is not the same")
        expected_error = "Invalid cabin class in lounge request"
        self.assertIn(expected_error, response.json()["ProcessingErrors"]["ProcessingError"]["Description"],
                      "Error description is not the same")







