import pytest
from utilities.BaseClass import BaseClass
from pageObjects.AjaxFormSubmitPage import AjaxFormSubmitPageClass
from pageObjects.JQueryDatePickerPage import JQueryDatePickerClass
from pageObjects.DownloadProgressBarPage import DownloadProgressBarClass
from pageObjects.RangeSlidersPage import RangeSlidersClass
from pageObjects.MultipleWindowPopupPage import MultipleWindowPopupClass
from pageObjects.AlertBoxPage import AlertBoxCheckClass
from pageObjects.FileDownloadPage import FileDownloadClass
from testdata.DataSource import DataProviderClass

from testcases.conftest import data_source_value

# due to some issues fetching data-source from commandline is not working properly now
# need to configure; time being below field can be set to excel, json to pick from corresponding sources
data_source_value = "excel"

class TestE2E(BaseClass):

    @pytest.mark.parametrize("get_data_ajax_input_form", DataProviderClass.get_data_for_testcase('ajax_form', data_source_value))
    def test_ajax_input_forms(self,get_data_ajax_input_form):
        logger = BaseClass.get_logger()
        logger.info("Testing Ajax Input Form Page ")

        ajax_page = AjaxFormSubmitPageClass(self.driver)
        ajax_page.open_ajax_form_submit()
        ajax_page.add_name_to_form(get_data_ajax_input_form["username"])
        ajax_page.add_comment_to_form(get_data_ajax_input_form["comments"])
        ajax_page.click_submit()
        ajax_page.check_spinner()
        ajax_page.check_submit_success_msg()

        logger.info("End fo Ajax Input Form Page Testing")

    @pytest.mark.parametrize("get_jquery_date_picker", DataProviderClass.get_data_for_testcase('jquery_date', data_source_value))
    def test_date_picker(self, get_jquery_date_picker):

        from_date = get_jquery_date_picker["from_date"]
        to_date = get_jquery_date_picker["to_date"]

        logger = BaseClass.get_logger()
        logger.info("Start of JQuery Date Picker Form Testing")

        date_picker_page = JQueryDatePickerClass(self.driver)
        date_picker_page.open_jquery_date_picker()
        date_picker_page.click_date_picker("from")
        date_picker_page.select_date(from_date)

        date_picker_page.click_date_picker("to")
        date_picker_page.select_date(to_date)

        logger.info("Verifying Negative Test case on To Date")
        date_picker_page.click_date_picker("to")
        date_picker_page.is_date_disabled(from_date, "to")

        logger.info("Verifying Negative Test case on From Date")
        date_picker_page.click_date_picker("from")
        date_picker_page.is_date_disabled(to_date, "from")

        logger.info("End fo JQuery Date Picker Form Page Testing")

    def test_progress_bars(self):
        logger = BaseClass.get_logger()
        logger.info("Start of Progress Bar Form Testing")
        progress_bar_page = DownloadProgressBarClass(self.driver)
        progress_bar_page.open_progress_bar_page()
        total_time = progress_bar_page.start_and_measure_download()
        logger.info("Download took {} seconds to complete".format(total_time))
        logger.info("End of Progress Bar Form Testing")

    @pytest.mark.parametrize("get_slider_range_picker",
                             DataProviderClass.get_data_for_testcase('slider_range', data_source_value))
    def test_sliders(self, get_slider_range_picker):
        print("Value is {}".format(get_slider_range_picker["value"]))
        logger = BaseClass.get_logger()
        logger.info("Start of Slider Bar Form Testing")
        sliders_page = RangeSlidersClass(self.driver)
        sliders_page.open_range_sliders_page()
        sliders_page.slide_all_sliders(get_slider_range_picker["value"])
        logger.info("End of Slider Bar Form Testing")

    def test_multiple_modal_windows(self):
        logger = BaseClass.get_logger()
        logger.info("Start of Modal Windows Testing")
        window_popup_page = MultipleWindowPopupClass(self.driver)
        window_popup_page.open_window_popup_page()
        window_popup_page.open_two_window_popup()
        logger.info("End of Modal Windows Testing")

    def test_js_alertbox(self):
        logger = BaseClass.get_logger()
        logger.info("Start of Alert Box Testing")
        alert_page = AlertBoxCheckClass(self.driver)
        alert_page.open_alert_boxes_page()
        alert_page.open_alert_box()
        logger.info("End of Alert Box Testing")

    @pytest.mark.parametrize("get_file_download_content_picker",
                             DataProviderClass.get_data_for_testcase('file_dw', data_source_value))
    def test_file_download(self, get_file_download_content_picker):
        logger = BaseClass.get_logger()
        logger.info("Start of File Download Testing")
        file_dw_page = FileDownloadClass(self.driver)
        file_dw_page.open_file_download_page()
        file_dw_page.enter_and_download_content(get_file_download_content_picker["content"])
        logger.info("End of File Download Testing")

