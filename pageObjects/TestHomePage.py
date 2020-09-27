from selenium.webdriver.common.by import By
from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException


class TestHomePage:

    DEMO_HOME_BUTTON = (By.LINK_TEXT, "Demo Home")
    DEMO_URL = "https://www.seleniumeasy.com/test/"
    SUBSCRIBE_WINDOW = (By.CSS_SELECTOR, "a[class*='cm-no-button']")
    TREE_MENU = (By.ID, "treemenu")
    SUBSCRIBE_WINDOW_CLOSED = False

    def __init__(self, driver):
        # self.driver = webdriver.Chrome()
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.driver.get('https://www.seleniumeasy.com/test')
        if not TestHomePage.SUBSCRIBE_WINDOW_CLOSED:
            self.close_subscribe_window()
        self.driver.refresh()

    def close_subscribe_window(self):
        try:
            self.wait.until(EC.element_to_be_clickable(TestHomePage.SUBSCRIBE_WINDOW))
            self.driver.find_element(*TestHomePage.SUBSCRIBE_WINDOW).click()
            TestHomePage.SUBSCRIBE_WINDOW_CLOSED = True
        except TimeoutException:
            print("Close Subscribe Window Not Found in given time")

    def open_home_page(self):
        self.driver.find_element(*TestHomePage.DEMO_HOME_BUTTON).click()
        self.wait.until(EC.url_contains(TestHomePage.DEMO_URL))
        assert self.driver.current_url == TestHomePage.DEMO_URL, "Demo Home Page Not Opened"

    def get_tree_menu(self):
        return self.driver.find_element(*TestHomePage.TREE_MENU)

