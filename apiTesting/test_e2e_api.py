from apiTesting.BookingClass import BookingClass
from testdata.DataSource import DataProviderClass
import pytest

data_source_value = "json"

class TestE2E():

    booking_id = None
    logger = None
    booking_info = {}

    @pytest.mark.parametrize("get_booking_data", DataProviderClass.get_data_for_testcase('booking_data', data_source_value, "api"))
    def test_api_create_new_booking(self, get_booking_data):
        booking = BookingClass()
        if not TestE2E.logger:
            TestE2E.logger = booking.logger
        TestE2E.logger.info("Start of Create New Booking Test Case")
        booking_data = get_booking_data
        TestE2E.booking_id = booking.create_new_booking(booking_data)
        if TestE2E.booking_id:
            TestE2E.booking_info[TestE2E.booking_id] = get_booking_data
        TestE2E.logger.info("End of Create New Booking Test Case")

    def test_api_get_booking(self):
        booking = BookingClass()
        if not TestE2E.logger:
            TestE2E.logger = booking.logger
        TestE2E.logger.info("Start of Get Booking Test Case")
        tmp = TestE2E.booking_info
        for key in TestE2E.booking_info.keys():
            booking.get_booking_by_id(key, TestE2E.booking_info[key])
        TestE2E.logger.info("End of Get Booking Test Case")

    @pytest.mark.parametrize("get_modified_data", DataProviderClass.get_data_for_testcase('modified_data', data_source_value, "api"))
    def test_api_modify_booking(self, get_modified_data):
        booking = BookingClass()
        if not TestE2E.logger:
            TestE2E.logger = booking.logger
        TestE2E.logger.info("Start of Modify Existing Booking Test Case")
        for key in TestE2E.booking_info.keys():
            booking.modify_booking(key, get_modified_data)
        TestE2E.logger.info("End of Modify Existing Booking Test Case")

    def test_api_delete_booking(self):
        booking = BookingClass()
        if not TestE2E.logger:
            TestE2E.logger = booking.logger
        TestE2E.logger.info("Start of Delete Booking Test Case")
        for key in TestE2E.booking_info.keys():
            booking.delete_booking(key)
        TestE2E.logger.info("End of Delete Booking Test Case")