from selenium.webdriver.common.by import By
from pageObjects.TestHomePage import TestHomePage
from utilities.BaseClass import BaseClass
import os
from time import sleep
import glob


class FileDownloadClass(BaseClass):

    ALERTS_AND_MODALS_LINK = (By.LINK_TEXT, "Alerts & Modals")
    FILE_DOWNLOAD_PAGE_LINK = (By.LINK_TEXT, "File Download")
    FILE_DOWNLOAD_VERIFICATION_ELEMENT = (By.TAG_NAME, "h2")
    FILE_DOWNLOAD_VERIFICATION_TEXT = "File Download Demo for Automation"
    TEXT_AREA_ELEMENT = (By.ID, "textbox")
    TEXT_STATUS_AREA = (By.ID, "textarea_feedback")
    CREATE_FILE_ELEMENT = (By.ID, "create")
    DOWNLOAD_FILE_ELEMENT = (By.ID, "link-to-download")
    FILE_DOWNLOAD_LOCATION = os.path.abspath("/Users/arun_rajamani/Downloads")
    FILE_NAME = "easyinfo.txt"
    FILE_NAME_PATTERN = "easyinfo*.txt"

    def __init__(self, driver):
        self.driver = driver
        self.homepage = TestHomePage(self.driver)
        self.logger = self.get_logger()

    def open_demo_home(self):
        self.homepage.open_home_page()
        return self.homepage

    def open_file_download_page(self):
        self.logger.info("Opening File Download Page")
        tree_menu_element = self.homepage.get_tree_menu()
        tree_menu_element.find_element(*FileDownloadClass.ALERTS_AND_MODALS_LINK).click()
        tree_menu_element.find_element(*FileDownloadClass.FILE_DOWNLOAD_PAGE_LINK).click()
        try:
            assert self.driver.find_element(*FileDownloadClass.FILE_DOWNLOAD_VERIFICATION_ELEMENT).text == \
                   FileDownloadClass.FILE_DOWNLOAD_VERIFICATION_TEXT
            self.driver.refresh()
        except AssertionError:
            self.logger.error("File Donwload Page cannot be opened")

    def enter_and_download_content(self, content):
        self.logger.info("Entering {} to the textarea".format(content))
        text_area_element = self.driver.find_element(*FileDownloadClass.TEXT_AREA_ELEMENT)
        text_area_element.send_keys(content)
        assert text_area_element.get_attribute("value") == content
        self.driver.find_element(*FileDownloadClass.TEXT_STATUS_AREA).click()

        self.logger.debug("Clicking on Create File")
        self.wait_for_clickable(FileDownloadClass.CREATE_FILE_ELEMENT)
        self.driver.find_element(*FileDownloadClass.CREATE_FILE_ELEMENT).click()

        self.logger.debug("Clicking on Download File")
        self.wait_for_clickable(FileDownloadClass.DOWNLOAD_FILE_ELEMENT)
        self.driver.find_element(*FileDownloadClass.DOWNLOAD_FILE_ELEMENT).click()

        try:
            # We wait maximum of 30 seconds for file to be downloaded
            for _ in range(30):
                file_path = os.path.join(FileDownloadClass.FILE_DOWNLOAD_LOCATION, FileDownloadClass.FILE_NAME)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as downlaoded_file:
                        try:
                            # restricting to first 500 characters
                            downloaded_content = downlaoded_file.read(500)
                            assert content == downloaded_content, "File Content mismatch"
                        except AssertionError:
                            self.logger.error("Content Mismatch")
                            self.logger.error("User Content {}".format(content))
                            self.logger.error("Downloaded Content {}".format(downloaded_content))
                    os.remove(file_path)
                    break
                else:
                    sleep(1)
            else:
                raise FileNotFoundError("File Not Downloaded")
        finally:
            self.logger.info("Clearing All Downloaded Files")
            for file in glob.glob(os.path.join(FileDownloadClass.FILE_DOWNLOAD_LOCATION, FileDownloadClass.FILE_NAME_PATTERN)):
                os.remove(file)
        return True
