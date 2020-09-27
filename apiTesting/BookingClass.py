from apiTesting.BaseClassFile import BaseClass
import json
import requests

class BookingClass(BaseClass):
    BASE_URL = 'https://restful-booker.herokuapp.com/booking'

    def __init__(self):
        self.logger = self.get_logger()

    def get_booking_by_id(self, booking_id, booking_data):
        self.logger.info("Getting Details For Booking ID: {}".format(booking_id))
        get_url = self.BASE_URL + '/' + str(booking_id)
        response = requests.get(get_url)
        try:
            assert response.status_code == 200
        except AssertionError:
            self.logger.error("GET Request Failed: Response is {}".format(response.status_code))
        try:
            res = response.json()
            assert self.dict_compare(booking_data, res)
        except AssertionError:
            self.logger.error("GET Request Failed: Data Mismatch Between")
            raise AssertionError
        self.logger.info("Found Details for booking id {}".format(response.content))

    def create_new_booking(self, booking_data):
        self.logger.info("Creating a new booking with following details {}".format(booking_data))
        response = requests.post(self.BASE_URL, json=booking_data)
        try:
            assert response.status_code == 200
        except AssertionError:
            self.logger.error("POST Request Failed: Response is {}".format(response.status_code))
            raise AssertionError
        try:
            txt = response.text
            resp_dict = json.loads(txt)
            assert self.dict_compare(booking_data, json.loads(response.text)['booking'])
        except AssertionError:
            self.logger.error("Create New Booking Failed because of data mismatch")
            raise AssertionError
        booking_id = response.json()['bookingid']
        self.logger.info("Booking Successful ID: {}".format(booking_id))
        return booking_id

    def _get_auth(self):
        self.logger.info("Authenticating the Sever with Credentials")
        auth_post_url = "https://restful-booker.herokuapp.com/auth"
        response = requests.post(url=auth_post_url,
                                 data={"username": "admin", "password": "password123"})
        try:
            assert response.status_code == 200
        except AssertionError:
            self.logger.error("Auth Request Failed: Response is {}".format(response.status_code))
        cookies = response.json()
        self.logger.info("Authentication Successful {}".format(cookies))
        return cookies

    def modify_booking(self, booking_id, booking_data):
        self.logger.info("Modifying Booking ID: {} with following details {}".format(booking_id, booking_data))
        cookies = self._get_auth()
        update_url = self.BASE_URL + '/' + str(booking_id)
        response = requests.put(update_url, json=booking_data, cookies=cookies)
        try:
            assert response.status_code == 200
        except AssertionError:
            self.logger.error("PUT Request Failed: Response is {}".format(response.status_code))
            raise AssertionError
        try:
            assert self.dict_compare(booking_data, json.loads(response.text))
        except AssertionError:
            self.logger.error("Modify Booking Failed because of data mismatch")
            raise AssertionError
        self.logger.info("Update Successful")
        return response.content

    def delete_booking(self, booking_id):
        self.logger.info("Deleting Booking ID {}".format(booking_id))
        cookies = self._get_auth()
        update_url = self.BASE_URL + '/' + str(booking_id)
        response = requests.delete(update_url, cookies=cookies)
        try:
            assert response.status_code == 201
        except AssertionError:
            self.logger.error("Delete Booking Failed for {}: Error Code".format(booking_id, response.status_code))
            raise AssertionError
        self.logger.info("Deletion Successful")

