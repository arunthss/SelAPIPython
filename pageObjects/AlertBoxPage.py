from selenium.webdriver.common.by import By
from pageObjects.TestHomePage import TestHomePage
from utilities.BaseClass import BaseClass
from selenium.common.exceptions import NoAlertPresentException

class AlertBoxCheckClass(BaseClass):

    ALERTS_AND_MODALS_LINK = (By.LINK_TEXT, "Alerts & Modals")
    JS_ALERTS_LINK = (By.LINK_TEXT, "Javascript Alerts")
    JS_ALERTS_VERIFICATION_ELEMENT = (By.TAG_NAME, "h3")
    JS_ALERTS_VERIFICATION_TEXT = "JavaScript has three kind of popup boxes: Alert box, Confirm box, and Prompt box."
    ALERT_BOX_ELEMENT_XPATH = (By.XPATH, "//p[contains(text(),'alert box')]/following-sibling::button")

    def __init__(self, driver):
        self.driver = driver
        self.homepage = TestHomePage(self.driver)
        self.logger = self.get_logger()

    def open_demo_home(self):
        self.homepage.open_home_page()
        return self.homepage

    def open_alert_boxes_page(self):
        self.logger.info("Opening Alert Boxes Page")
        tree_menu_element = self.homepage.get_tree_menu()
        tree_menu_element.find_element(*AlertBoxCheckClass.ALERTS_AND_MODALS_LINK).click()
        tree_menu_element.find_element(*AlertBoxCheckClass.JS_ALERTS_LINK).click()
        assert self.driver.find_element(*AlertBoxCheckClass.JS_ALERTS_VERIFICATION_ELEMENT).text == \
               AlertBoxCheckClass.JS_ALERTS_VERIFICATION_TEXT
        self.driver.refresh()

    def open_alert_box(self):
        self.driver.find_element(*AlertBoxCheckClass.ALERT_BOX_ELEMENT_XPATH).click()
        try:
            self.wait_for_alert()
            alert_text = self.driver.switch_to.alert.text
            self.driver.switch_to.alert.accept()
            self.logger.info("Alert Text Found is {}".format(alert_text))
            return alert_text
        except NoAlertPresentException:
            self.logger.error("No Alert Box Found")
