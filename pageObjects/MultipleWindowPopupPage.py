from selenium.webdriver.common.by import By
from pageObjects.TestHomePage import TestHomePage
from utilities.BaseClass import BaseClass


class MultipleWindowPopupClass(BaseClass):

    ALERTS_AND_MODALS_LINK = (By.LINK_TEXT, "Alerts & Modals")
    WINDOW_POPUP_LINK = (By.LINK_TEXT, "Window Popup Modal")
    WINDOW_POPUP_VERIFICATION_ELEMENT = (By.TAG_NAME, "h2")
    WINDOW_POPUP_VERIFICATION_TEXT = "Window popup Modal Example for Automation"
    TWO_WINDOW_POPUP_XPATH = (By.XPATH, "//div[@class='two-windows']/a")

    def __init__(self, driver):
        self.driver = driver
        self.homepage = TestHomePage(self.driver)
        self.logger = self.get_logger()

    def open_demo_home(self):
        self.homepage.open_home_page()
        return self.homepage

    def open_window_popup_page(self):
        self.logger.info("Opening Windows Popup Page")
        tree_menu_element = self.homepage.get_tree_menu()
        tree_menu_element.find_element(*MultipleWindowPopupClass.ALERTS_AND_MODALS_LINK).click()
        tree_menu_element.find_element(*MultipleWindowPopupClass.WINDOW_POPUP_LINK).click()
        assert self.driver.find_element(*MultipleWindowPopupClass.WINDOW_POPUP_VERIFICATION_ELEMENT).text == \
               MultipleWindowPopupClass.WINDOW_POPUP_VERIFICATION_TEXT
        self.driver.refresh()

    def open_two_window_popup(self):
        parent_window = self.driver.window_handles[0]
        self.logger.info("Opening Two Window Popup Link")
        self.driver.find_element(*MultipleWindowPopupClass.TWO_WINDOW_POPUP_XPATH).click()
        self.wait_for_window_count(3)
        self.logger.info("Two New Windows Opened")
        window_titles = []
        for window in self.driver.window_handles:
            if parent_window != window:
                self.driver.switch_to.window(window)
                win_title = self.driver.title
                self.logger.info("Window Title is {}".format(win_title))
                window_titles.append(win_title)
                self.driver.close()
        self.driver.switch_to.window(parent_window)
        win_title = self.driver.title
        self.logger.info("Parent Window Title is {}".format(win_title))
        window_titles.append(win_title)
        self.logger.info("All Windows Titles are {}".format(window_titles))
        return window_titles
