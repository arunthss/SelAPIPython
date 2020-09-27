import pytest
from selenium import webdriver

data_source_value = None
driver = None
test_type_value = None


def pytest_addoption(parser):
    parser.addoption(
        "--type", action="store", default="selenium",
    )
    parser.addoption(
        "--browser_name", action="store", default="chrome",
    )
    parser.addoption(
        "--data_source", action="store", default="local",
    )


@pytest.fixture(scope='class')
def setup(request):
    test_type = request.config.getoption('type')
    test_type = str(test_type).lower().strip()
    if test_type == "selenium":
        global test_type_value
        test_type_value = "selenium"
        browser_name = request.config.getoption("browser_name")
        browser_name = str(browser_name).lower().strip()
        print("Browser is", browser_name)
        global driver
        if browser_name == "chrome":
            driver = webdriver.Chrome(executable_path='../drivers/chromedriver')
        elif browser_name == "firefox":
            driver = webdriver.Firefox(executable_path='../drivers/geckodriver')
        elif browser_name == 'edge-chromium':
            options = dict()
            options['use_chromium']= True
            options['binary_location'] = r'/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge'
            driver = webdriver.Edge(executable_path='../drivers/msedgedriver',capabilities=options)

        data_source = request.config.getoption("data_source")
        data_source = str(data_source).lower().strip()
        global data_source_value
        print("Data Source is", data_source)
        if data_source == "excel":
            data_source_value = "excel"
        elif data_source == "json":
            data_source_value = "json"
        else:
            data_source_value = "local"

        driver.implicitly_wait(time_to_wait=10)
        driver.maximize_window()
        driver.get('https://www.seleniumeasy.com/test')
        request.cls.driver = driver
    else:
        # no actions defined for API testcases now
        pass
    yield

    if driver:
        driver.close()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    global test_type_value
    if test_type_value == "selenium":
        pytest_html = item.config.pluginmanager.getplugin('html')
        outcome = yield
        report = outcome.get_result()
        extra = getattr(report, 'extra', [])

        if report.when == 'call' or report.when == "setup":
            xfail = hasattr(report, 'wasxfail')
            if (report.skipped and xfail) or (report.failed and not xfail):
                file_name = report.nodeid.replace("::", "_") + ".png"
                _capture_screenshot(file_name)
                if file_name:
                    html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                           'onclick="window.open(this.src)" align="right"/></div>' % file_name
                    extra.append(pytest_html.extras.html(html))
            report.extra = extra


def _capture_screenshot(name):
    if driver:
        driver.get_screenshot_as_file(name)

