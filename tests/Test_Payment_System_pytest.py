# import unittest

import pytest
# import allure
from selenium.webdriver.android.webdriver import WebDriver

from page.Login_Page import Login_Page
from utils.ConfigHelper import ConfigHelper
from utils.DriverFactory import DriverFactory


# test_data_payment_system = [("VISA, MasterCard, Maestro"), ("Neteller"), ("Skrill"), ("Perfect Money"), ("Fasapay"), ("WebMoney"), ("Payweb"), ("Яндекс.Деньги"), ("VISA, MasterCard, Visa Electron")]


@pytest.fixture(scope="module")
def get_driver():
    """setUp / teaeDown"""
    driver = DriverFactory().get_web_driver("chrome")
    login = ConfigHelper().getConfigOption('username1_valid', 'login')
    password = ConfigHelper().getConfigOption("username1_valid", "password")
    login_page = Login_Page(selenium_driver=driver)
    payment_page = login_page.login(login, password)

    # def teardown():
    #    driver.close()
    #    request.addfinalizer(teardown)
    # return payment_page

    yield driver
    driver.close()
    # @pytest.mark.parametrize(['Neteller','Payweb'])


# @pytest.fixture(['Neteller', 'Payweb'])
@pytest.mark.parametrize('paym', ["Payweb", "Perfect Money", 'Neteller'])
def test_payment_system(get_driver : WebDriver, paym):
    """изменяем систему оплаты и см результат"""
    get_driver.get("https://ibitcy.com/interview/qa/mobile-deposit/#/payment")
    payment_page.select_payment_system(paym)
    proceed_page = payment_page.submit_payment()
    result_text = proceed_page.get_message_result()
    print(result_text)
    assert "YOUR PAYMENT IS BEING PROCESSED" == result_text, "нет ошибки"



