from selenium.webdriver.common.by import By
from pageObjects.TestHomePage import TestHomePage
from utilities.BaseClass import BaseClass
from time import perf_counter


class DownloadProgressBarClass(BaseClass):

    PROGRESS_BAR_AND_SLIDERS_LINK = (By.LINK_TEXT, "Progress Bars & Sliders")
    JQUERY_DOWNLOAD_PROGRESS_BAR_LINK = (By.LINK_TEXT, "JQuery Download Progress bars")
    DOWNLOAD_PROGRESS_BAR_VERIFICATION_ELEMENT = (By.TAG_NAME, "h2")
    DOWNLOAD_PROGRESS_BAR_VERIFICATION_TEXT = "JQuery UI Progress bar - Download Dialog"
    DOWNLOAD_BUTTON_ELEMENT = (By.ID, "downloadButton")
    DOWNLOAD_STATUS_ELEMENT = (By.CLASS_NAME,"ui-dialog-title")
    DOWNLOAD_PROGRESS_LABEL = (By.CLASS_NAME, "progress-label")

    def __init__(self, driver):
        self.driver = driver
        self.homepage = TestHomePage(self.driver)
        self.logger = self.get_logger()

    def open_progress_bar_page(self):
        self.logger.info("Opening Progress Bar Page")
        tree_menu_element = self.homepage.get_tree_menu()
        tree_menu_element.find_element(*DownloadProgressBarClass.PROGRESS_BAR_AND_SLIDERS_LINK).click()
        tree_menu_element.find_element(*DownloadProgressBarClass.JQUERY_DOWNLOAD_PROGRESS_BAR_LINK).click()
        assert self.driver.find_element(*DownloadProgressBarClass.DOWNLOAD_PROGRESS_BAR_VERIFICATION_ELEMENT).text == \
            DownloadProgressBarClass.DOWNLOAD_PROGRESS_BAR_VERIFICATION_TEXT
        self.driver.refresh()

    def start_and_measure_download(self):
        self.logger.info("Starting Download..")
        self.driver.find_element(*DownloadProgressBarClass.DOWNLOAD_BUTTON_ELEMENT).click()
        try:
            self.wait_for_presence(DownloadProgressBarClass.DOWNLOAD_STATUS_ELEMENT)
        except TimeoutError:
            self.logger.info("At times download dont start on one click, adding another click here")
            self.driver.find_element(*DownloadProgressBarClass.DOWNLOAD_BUTTON_ELEMENT).click()
            self.wait_for_presence(DownloadProgressBarClass.DOWNLOAD_STATUS_ELEMENT)

        start_time = perf_counter()
        self.logger.info("Start Time {}".format(start_time))
        progress_element = self.driver.find_element(*DownloadProgressBarClass.DOWNLOAD_PROGRESS_LABEL)
        previous_state = None
        current_state = progress_element.text

        while current_state != 'Complete!':
            if current_state != previous_state:
                print(current_state)
                previous_state = current_state
            current_state = progress_element.text

        self.logger.info("Download Complete!!")
        end_time = perf_counter()
        self.logger.info("End Time {}".format(end_time))
        total_time = end_time - start_time
        self.logger.info("Total Time Elapsed {} seconds".format(total_time))
        return total_time

