import unittest

from page.Login_Page import Login_Page
from utils.ConfigHelper import ConfigHelper
from utils.DriverFactory import DriverFactory

test_data_payment_system = [
    ("VISA, MasterCard, Maestro"),
    ("Neteller"),
    ("Skrill"),
    ("Perfect Money"),
    ("Fasapay"),
    ("WebMoney"),
    ("Payweb"),
    ("Яндекс.Деньги"),
    ("VISA, MasterCard, Visa Electron")
]

def test_payment_system(paym):
    def _test_func(self):
        """изменяем систему оплаты и см результат"""
        self.payment_page.select_payment_system(paym)
        proceed_page = self.payment_page.submit_payment()
        result_text = proceed_page.get_message_result()
        print(result_text)

    return _test_func


class TestPaymSys(unittest.TestCase):

    def setUp(self):
        self.driver = DriverFactory().get_web_driver("chrome")
        login = ConfigHelper().getConfigOption('username1_valid', 'login')
        password = ConfigHelper().getConfigOption("username1_valid", "password")
        login_page = Login_Page(selenium_driver=self.driver)
        self.payment_page = login_page.login(login, password)

    def tearDown(self):
        self.driver.close()

for i, (paym) in enumerate(test_data_payment_system):
    setattr(TestPaymSys, 'test("{0}")'.format(paym),  test_payment_system(paym))

if __name__ == "__main__":
    unittest.main()