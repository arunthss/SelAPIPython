import pytest
import logging
import inspect
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from testdata.DataSource import DataProviderClass

@pytest.mark.usefixtures('setup')
class BaseClass:
    wait = None

    @staticmethod
    def get_logger():
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        fmt = logging.Formatter("%(asctime)s: %(levelname)s %(name)s: %(message)s")
        file_handler = logging.FileHandler('../results/sel_automation.log','a')
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger

    def wait_for_presence(self, locator, wait_time=10):
        if not BaseClass.wait:
            BaseClass.wait = WebDriverWait(self.driver, wait_time)
        BaseClass.wait.until(EC.presence_of_element_located(locator))

    def wait_for_window_count(self, window_count, wait_time=10):
        if not BaseClass.wait:
            BaseClass.wait = WebDriverWait(self.driver, wait_time)
        BaseClass.wait.until(EC.number_of_windows_to_be(window_count))

    def wait_for_alert(self, wait_time=10):
        if not BaseClass.wait:
            BaseClass.wait = WebDriverWait(self.driver, wait_time)
        BaseClass.wait.until(EC.alert_is_present())

    def wait_for_clickable(self, locator, wait_time=10):
        if not BaseClass.wait:
            BaseClass.wait = WebDriverWait(self.driver, wait_time)
        BaseClass.wait.until(EC.element_to_be_clickable(locator))

    def select_element(self, locator, select_type, select_value):
        self.select = Select(self.driver.find_element(*locator))
        if select_type == 'visible_text':
            self.select.select_by_visible_text(select_value)
        elif select_type == 'index':
            self.select.select_by_index(select_value)
        elif select_type == 'value':
            self.select.deselect_by_value(select_value)
        else:
            print("Unsupported Selection Format {}".format(select_type))

    def get_select_options(self):
        return self.select.options

    def populate_data_source(self, source):
        if source == "excel":
            DataProviderClass.populate_data_from_excel()
        elif source == "json":
            DataProviderClass.populate_data_from_json()
