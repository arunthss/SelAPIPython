from selenium.webdriver.common.by import By
from pageObjects.TestHomePage import TestHomePage
from utilities.BaseClass import BaseClass
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep


class RangeSlidersClass(BaseClass):

    PROGRESS_BAR_AND_SLIDERS_LINK = (By.LINK_TEXT, "Progress Bars & Sliders")
    DRAG_AND_DROP_SLIDERS_LINK = (By.LINK_TEXT, "Drag & Drop Sliders")
    RANGE_SLIDERS_VERIFICATION_ELEMENT = (By.TAG_NAME, "h2")
    RANG_SLIDERS_VERIFICATION_TEXT = "Range Sliders"
    SLIDERS_DIV_XPATH = (By.XPATH, "//div//input[@type='range']/parent::div")

    def __init__(self, driver):
        self.driver = driver
        self.homepage = TestHomePage(self.driver)
        self.logger = self.get_logger()

    def open_range_sliders_page(self):
        self.logger.info("Opening Range Sliders Page")
        tree_menu_element = self.homepage.get_tree_menu()
        tree_menu_element.find_element(*RangeSlidersClass.PROGRESS_BAR_AND_SLIDERS_LINK).click()
        tree_menu_element.find_element(*RangeSlidersClass.DRAG_AND_DROP_SLIDERS_LINK).click()
        assert self.driver.find_element(*RangeSlidersClass.RANGE_SLIDERS_VERIFICATION_ELEMENT).text == \
               RangeSlidersClass.RANG_SLIDERS_VERIFICATION_TEXT
        self.driver.refresh()

    def slide_all_sliders(self, value=50):
        self.logger.info("Sliding for value {}".format(value))
        value = int(value)
        print("Sliding for {}".format(value))
        action = ActionChains(self.driver)
        slider_div_elements = self.driver.find_elements(*RangeSlidersClass.SLIDERS_DIV_XPATH)

        for slider in slider_div_elements:
            range_val = slider.find_element(By.TAG_NAME, "output")
            slider_input = slider.find_element(By.TAG_NAME, "input")

            # Seeing some inconsistent behaviour while working with pytest,
            # like the other sliders moves a bit while changing a different one
            # tried different workarounds, but this issue is still seen
            # invoking below code without pytest works just fine and smooth

            slider_input.click()
            sleep(1)
            start_offset = slider_input.size["width"] / 2
            action.move_to_element_with_offset(slider_input, start_offset, 0).click().perform()

            output_val = int(range_val.get_attribute("value"))
            while output_val != value:
                if output_val < value:
                    action.send_keys(Keys.ARROW_RIGHT).perform()
                else:
                    action.send_keys(Keys.ARROW_LEFT).perform()
                output_val = int(range_val.get_attribute("value"))

        try:
            assert output_val == value, "Could not slide to value {}".format(value)
            self.logger.info("Slided to Value {}".format(value))
        except AssertionError:
            self.logger.error("Could Not Slide to Value {}".format(value))
