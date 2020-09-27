# SelAPIPython
Selenium and API automation draft using python

1. Please install following python libraries
* requests
* selenium
* openpyxl
* pytest
* pytest-html

2. Add browser drivers to drivers folder

3. run following commands in terminal/ configure pycharm configurations
Selenium Runs -  py.test testcases/test_e2e_selenium.py -s -v --html=report.html --browser_name=chrome
API Runs - py.test apiTesting/test_e2e_api.py -s -v

Note: Currently we see some errors while running from terminal, which works fine with pycharm
