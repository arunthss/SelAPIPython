from selenium.webdriver.common.by import By
from pageObjects.TestHomePage import TestHomePage
from datetime import datetime, timedelta
from utilities.BaseClass import BaseClass


class JQueryDatePickerClass(BaseClass):
    MONTH_NAME_LIST = ["","Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    DATE_PICKER_LINK = (By.LINK_TEXT, "Date pickers")
    JQUERY_DATE_PICKER_LINK = (By.LINK_TEXT, "JQuery Date Picker")
    JQUERY_DATE_PICKER_VERIFICATION_ELEMENT = (By.TAG_NAME, "h2")
    JQUERY_DATE_PICKER_VERIFICATION_TEXT = "JQuery Date Picker Demo"
    FROM_DATE_ELEMENT = (By.ID, "from")
    TO_DATE_ELEMENT = (By.ID, "to")
    DATE_PICKER_ELEMENT = (By.CLASS_NAME, "ui-datepicker-month")
    DAY_PICKER_ELEMENT = (By.XPATH, "//table[@class='ui-datepicker-calendar']//td/a")
    FROM_DATE_ELEMENT_LABEL = (By.XPATH, "//label[contains(text(),'From')]")
    ENABLED_MONTH_XPATH = (By.XPATH, "//*[@class='ui-datepicker-month']/option")
    ENABLED_DAYS_XPATH = (By.XPATH, "//table[@class='ui-datepicker-calendar']//td/a")

    def __init__(self, driver):
        self.driver = driver
        self.homepage = TestHomePage(self.driver)
        self.logger = self.get_logger()

    def open_demo_home(self):
        self.homepage.open_home_page()
        return self.homepage

    def open_jquery_date_picker(self):
        self.logger.info("Opening JQuery Date Picker Page")
        tree_menu_element = self.homepage.get_tree_menu()
        tree_menu_element.find_element(*JQueryDatePickerClass.DATE_PICKER_LINK).click()
        tree_menu_element.find_element(*JQueryDatePickerClass.JQUERY_DATE_PICKER_LINK).click()
        assert self.driver.find_element(*JQueryDatePickerClass.JQUERY_DATE_PICKER_VERIFICATION_ELEMENT).text == \
               JQueryDatePickerClass.JQUERY_DATE_PICKER_VERIFICATION_TEXT
        self.driver.refresh()

    def click_date_picker(self, date_type):
        self.logger.info("Clicking on Date Picker Field")
        if date_type == 'from':
            self.date_element = self.driver.find_element(*JQueryDatePickerClass.FROM_DATE_ELEMENT)
        else:
            self.date_element = self.driver.find_element(*JQueryDatePickerClass.TO_DATE_ELEMENT)
        self.date_element.click()
        try:
            self.wait_for_presence(JQueryDatePickerClass.DATE_PICKER_ELEMENT)
        except Exception:
            self.logger.info("Date Picker Not Present on page, Trying one more time")
            self.driver.find_element(*JQueryDatePickerClass.FROM_DATE_ELEMENT_LABEL).click()
            self.wait_for_presence(JQueryDatePickerClass.DATE_PICKER_ELEMENT)
            self.logger.info("Date Picker Found on page")

    def select_date(self, date_input):
        self.logger.info("Selecting {} From Date Picker".format(date_input))
        actual_date = datetime.fromisoformat(date_input)
        self.wait_for_presence(JQueryDatePickerClass.DATE_PICKER_ELEMENT)
        self.select_month(JQueryDatePickerClass.MONTH_NAME_LIST[actual_date.month])
        date_elements = self.driver.find_elements(*JQueryDatePickerClass.DAY_PICKER_ELEMENT)
        date_elements[actual_date.day - 1].click()
        processed_date_format = "{:02}/{:02}/{}".format(actual_date.month,
                                                  actual_date.day,
                                                  actual_date.year)
        actual_date_format = self.date_element.get_attribute("value")
        assert processed_date_format == actual_date_format, "Date Mismatch"
        self.logger.info("{} {} Matched".format(processed_date_format,actual_date_format))

    def select_month(self, month_abbr):
        self.select_element(JQueryDatePickerClass.DATE_PICKER_ELEMENT,"visible_text",month_abbr)

    def is_date_disabled(self, date_input, date_type):
        self.logger.info("Checking if date field is disabled")
        actual_date = datetime.fromisoformat(date_input)
        self.wait_for_presence(JQueryDatePickerClass.DATE_PICKER_ELEMENT)
        if date_type == 'from':
            self.select_month(JQueryDatePickerClass.MONTH_NAME_LIST[actual_date.month])
            enabled_days = self.driver.find_elements(*JQueryDatePickerClass.ENABLED_DAYS_XPATH)
            try:
                assert len(enabled_days) == actual_date.day
                self.logger.info("Assertion Success on From Field")
            except AssertionError:
                self.logger.error("From {} date is not disabled".format(date_input))
        elif date_type == 'to':
            first_enabled_month = self.driver.find_elements(By.XPATH, "//option")[0].get_attribute("text")
            try:
                assert first_enabled_month == JQueryDatePickerClass.MONTH_NAME_LIST[actual_date.month]
                self.logger.info("Assertion Success on To Field")
            except AssertionError:
                self.logger.error("To {} date is not disabled".format(date_input))

    @staticmethod
    def get_date_offset(date_input, offset):
        date_input = datetime.fromisoformat(date_input)
        delta = timedelta(offset)
        return date_input + delta

