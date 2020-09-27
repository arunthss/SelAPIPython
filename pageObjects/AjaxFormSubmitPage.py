from selenium.webdriver.common.by import By
from pageObjects.TestHomePage import TestHomePage
from utilities.BaseClass import BaseClass

class AjaxFormSubmitPageClass(BaseClass):

    INPUT_FORMS_LINK = (By.LINK_TEXT, "Input Forms")
    AJAX_FORM_SUBMIT_LINK = (By.LINK_TEXT, "Ajax Form Submit")
    AJAX_FORM_SUBMIT_VERIFICATION_ELEMENT = (By.XPATH, "//h1[contains(text(),'Ajax Form Submit with Loading icon')]")
    AJAX_FORM_NAME_ELEMENT = (By.ID, "title")
    AJAX_FORM_COMMENT_ELEMENT = (By.ID, "description")
    AJAX_FORM_SUBMIT_ELEMENT = (By.ID, "btn-submit")
    AJAX_FORM_SUBMIT_SPINNER_ELEMENT = (By.CSS_SELECTOR, "img[src='LoaderIcon.gif']")
    AJAX_FORM_SUBMIT_SUCCESS_STATUS_ELEMENT = (By.XPATH, "//div[text()='Form submited Successfully!']")

    def __init__(self, driver):
        self.driver = driver
        self.homepage = TestHomePage(self.driver)
        self.logger = self.get_logger()

    def open_demo_home(self):
        self.homepage.open_home_page()
        return self.homepage

    def open_ajax_form_submit(self):
        self.logger.info("Opening Ajax Form Submit Page")
        tree_menu_element = self.homepage.get_tree_menu()
        tree_menu_element.find_element(*AjaxFormSubmitPageClass.INPUT_FORMS_LINK).click()
        tree_menu_element.find_element(*AjaxFormSubmitPageClass.AJAX_FORM_SUBMIT_LINK).click()
        try:
            assert self.driver.find_element(*AjaxFormSubmitPageClass.AJAX_FORM_SUBMIT_VERIFICATION_ELEMENT), \
            "Ajax Form Submit Page Not Found"
        except AssertionError:
            self.logger.error("Ajax Form Submit Page Not Found")
        self.driver.refresh()

    def add_name_to_form(self, name):
        self.logger.info("Adding Name {} to the form".format(name))
        name_element = self.driver.find_element(*AjaxFormSubmitPageClass.AJAX_FORM_NAME_ELEMENT)
        name_element.send_keys(name)
        assert name_element.get_attribute('value') == name, "Name Mismatch Found"

    def add_comment_to_form(self, comment):
        self.logger.info("Adding Comment {} to the form".format(comment))
        comment_element = self.driver.find_element(*AjaxFormSubmitPageClass.AJAX_FORM_COMMENT_ELEMENT)
        comment_element.send_keys(comment)
        assert comment_element.get_attribute('value') == comment, "Comments mismatch Found"

    def click_submit(self):
        self.logger.debug("Clicking on submit button")
        self.driver.find_element(*AjaxFormSubmitPageClass.AJAX_FORM_SUBMIT_ELEMENT).click()

    def check_spinner(self):
        self.logger.info("Checking for Spinner Button")
        try:
            assert self.driver.find_element(*AjaxFormSubmitPageClass.AJAX_FORM_SUBMIT_SPINNER_ELEMENT), "Spinner Not Found"
        except AssertionError:
            self.logger.error("Spinner Button Not Found")

    def check_submit_success_msg(self):
        self.logger.info("Checking for Success Message")
        try:
            assert self.driver.find_element(*AjaxFormSubmitPageClass.AJAX_FORM_SUBMIT_SUCCESS_STATUS_ELEMENT), "Success Message Not Found"
        except AssertionError:
            self.logger.error("Success Message Not Found")

