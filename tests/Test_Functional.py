#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import unittest
from page.Login_Page import Login_Page
from utils.ConfigHelper import ConfigHelper
from utils.DriverFactory import DriverFactory


class Ibit_Test(unittest.TestCase):
    def setUp(self):
        self.driver = DriverFactory().get_web_driver("chrome")
        login = ConfigHelper().getConfigOption('username1_valid', 'login')
        password = ConfigHelper().getConfigOption("username1_valid", "password")
        login_page = Login_Page(selenium_driver=self.driver)
        self.payment_page = login_page.login(login, password)

    def tearDown(self):
        self.driver.close()

    def test_qiwi_phone_negativ(self):
        """негативная проверка ввода телефона при оплате с qiwi"""
        phone = "+70"
        self.payment_page.select_payment_system("QIWI")
        self.payment_page.submit_payment(False)
        self.payment_page.qiwi_set_phone(phone)
        proceed_page = self.payment_page.qiwi_submit(True)
        is_error = self.payment_page.is_error_qiwi_phone()
        self.payment_page.qiwi_close()
        self.assertTrue(is_error, "Должна быть ошибка в форме ввода телефона")

    def test_qiwi_phone_positive(self):
        """позитивная проверка ввода телефона при оплате с qiwi"""
        phone = "+79271591181"
        expected_result = "YOUR PAYMENT IS BEING PROCESSED"
        self.payment_page.select_payment_system("QIWI")
        self.payment_page.submit_payment(False)
        self.payment_page.qiwi_set_phone(phone)
        proceed_page = self.payment_page.qiwi_submit()
        result_text = proceed_page.get_message_result()
        self.payment_page = proceed_page.goto_forvard()
        self.assertEqual(result_text, expected_result, "Ожидаем статус по процессу оплаты")

    def test_qiwi_phone_forvard(self):
        """оплата через Киви - отмена"""
        self.payment_page.select_payment_system("QIWI")
        self.payment_page.submit_payment(False)
        time.sleep(2)
        qiwi_visible = self.payment_page.is_qiwi_visible()
        self.assertTrue(qiwi_visible, "Должны видеть панель Киви")
        self.payment_page.qiwi_close()
        qiwi_visible = self.payment_page.is_qiwi_visible()
        self.assertFalse(qiwi_visible, "не Должны видеть панель Киви")

    def test_currency_active_status(self):
        """переключаемся между валютами и проверяем активный статус"""
        self.payment_page.set_amount_value(1000)
        currency = "USD"
        self.payment_page.select_currency(currency)
        active_status = self.payment_page.get_active_status()
        currency_actual = self.payment_page.get_value_currency()
        self.assertTrue(currency in currency_actual, "Ожидается выбранная валюта")
        self.assertEqual(active_status.lower(), "gold", "ожидается актуальный статус - обводка")
        print("active status: %s" % active_status)

        currency = "RUB"
        self.payment_page.select_currency(currency)
        active_status = self.payment_page.get_active_status()
        currency_actual = self.payment_page.get_value_currency()
        self.assertTrue(currency in currency_actual, "Ожидается выбранная валюта")
        self.assertEqual(active_status.lower(), "micro", "ожидается актуальный статус - обводка")
        print("active status: %s" % active_status)

        currency = "CNH"
        self.payment_page.select_currency(currency)
        active_status = self.payment_page.get_active_status()
        currency_actual = self.payment_page.get_value_currency()
        self.assertTrue(currency in currency_actual, "Ожидается выбранная валюта")
        self.assertEqual(active_status.lower(), "micro", "ожидается актуальный статус - обводка")
        print("active status: %s" % active_status)

    def test_view_pricing(self):
        """проверяем страницу по статусам трейдеров"""
        pricing_page = self.payment_page.goto_pricing()
        header = pricing_page.get_header()
        self.assertEqual(header, "TRADERS CHOICE", "Должны обнаружить на стр прайсов,трейдеров")
        payment_page = pricing_page.goto_payment()

    def test_view_pricing_back(self):
        """проверяем после страницы по статусам трейдеров - старые значения"""

        self.payment_page.select_payment_system("WebMoney")
        self.payment_page.select_currency("RUB")
        self.payment_page.set_amount_value(25000)
        self.payment_page.check_bonus()

        actual_state = self.payment_page.get_active_status()
        payment_system = self.payment_page.get_value_payment_system()
        currency = self.payment_page.get_value_currency()
        youget = self.payment_page.get_you_get()
        amount = self.payment_page.get_amount_value()
        bonus_state = self.payment_page.get_state_bonus()
        bonus_value = self.payment_page.get_bonus_value()
        cur_param = [actual_state, payment_system, currency, youget, amount, bonus_state, bonus_value]

        pricing_page = self.payment_page.goto_pricing()
        header = pricing_page.get_header()
        self.assertEqual(header, "TRADERS CHOICE", "Должны обнаружить на стр прайсов,трейдеров")
        self.payment_page = pricing_page.goto_payment()

        actual_state = self.payment_page.get_active_status()
        payment_system = self.payment_page.get_value_payment_system()
        currency = self.payment_page.get_value_currency()
        youget = self.payment_page.get_you_get()
        amount = self.payment_page.get_amount_value()
        bonus_state = self.payment_page.get_state_bonus()
        bonus_value = self.payment_page.get_bonus_value()
        new_param = [actual_state, payment_system, currency, youget, amount, bonus_state, bonus_value]

        self.assertEqual(new_param, cur_param, "Должны сохраниться значения при возврате")

    def test_calc_bonus(self):
        """рассчитывать бонус, изменение ю гет"""
        bonus_state = self.payment_page.get_state_bonus()
        bonus_value = self.payment_page.get_bonus_value()
        self.payment_page.check_bonus()
        self.assertNotEqual(bonus_state, self.payment_page.get_state_bonus())
        self.assertNotEqual(bonus_value, self.payment_page.get_bonus_value())

        amount = 666
        self.payment_page.set_amount_value(amount)
        self.payment_page.check_bonus()
        self.assertEqual(True, self.payment_page.get_state_bonus())
        self.assertEqual(self.payment_page.get_you_get(), str(amount * 2))

    def test_select_status(self):
        """прощелкиваем статусы"""
        currency = "USD"
        states = ["mini", "silver", "vip", "gold"]
        self.payment_page.select_currency(currency)

        self.payment_page.select_status(states[0])
        self.assertEqual(self.payment_page.get_amount_value(), str(200), "Пороговые значения, в соотв со статусом")

        self.payment_page.select_status(states[1])
        self.assertEqual(self.payment_page.get_amount_value(), str(500), "Пороговые значения, в соотв со статусом")

        self.payment_page.select_status(states[2])
        self.assertEqual(self.payment_page.get_amount_value(), str(2500), "Пороговые значения, в соотв со статусом")

        self.payment_page.select_status(states[3])
        self.assertEqual(self.payment_page.get_amount_value(), str(1000), "Пороговые значения, в соотв со статусом")

    # надо сделать - массив подавать
    def test_payment_system_payweb(self):
        """изменяем систему оплаты и см результат"""
        self.payment_page.select_payment_system("Payweb")
        proceed_page = self.payment_page.submit_payment()
        result_text = proceed_page.get_message_result()
        print(result_text)


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = DriverFactory().get_web_driver("chrome")

    def tearDown(self):
        self.driver.close()

    @unittest.SkipTest
    def test_ibit_login(self):  # browser="chrome"
        "авторизация тестовыми наборами тест пользователей"

        login = ConfigHelper().getConfigOption('username1_valid', 'login')
        password = ConfigHelper().getConfigOption("username1_valid", "password")

        # убрал PageFactory
        # loginPage = PageFactory().getPageObject("login page", self.driver)

        login_page = Login_Page(selenium_driver=self.driver)
        payment_page = login_page.login(login, password)

        payment_page.select_status("mini")
        payment_page.select_payment_system("Payweb")
        proceed_page = payment_page.submit_payment()
        result_text = proceed_page.get_message_result()
        print(result_text)
        payment_page = proceed_page.goto_forvard()

        '''
        print("bonus state before check: {0}".format(payment_page.get_state_bonus()))
        payment_page.check_bonus()
        print("bonus state after check: {0}".format(payment_page.get_state_bonus()))
        print("bonus value: %s" % payment_page.get_bonus_value())
        print("you get value: %s" % payment_page.get_you_get())

        print("amount: %s" % payment_page.get_amount_value())
        payment_page.set_amount_value(666)  # 999.2 граничные значения, дробные, отрицыт
        print("active status: %s" % payment_page.get_active_status())

        payment_system = "WebMoney"
        payment_page.select_payment_system(payment_system)
        payment_system_actual = payment_page.get_value_payment_system()
        self.assertEqual(payment_system_actual, payment_system, "Ожидаем плат систему")
        
        time.sleep(2)
        pricing_page = payment_page.goto_pricing()
        time.sleep(2)
        payment_page = pricing_page.goto_payment()
        time.sleep(2)
        
        currency = "CNH"
        payment_page.select_currency(currency)
        currency_actual = payment_page.get_value_currency()
        self.assertTrue(currency in currency_actual, "Ожидается выбранная валюта")
        
        #
        payment_page.select_payment_system("QIWI")
        payment_page.submit_payment(False)
        time.sleep(2)
        payment_page.qiwi_close()
        
        # ошибка ввода телефона qiwi
        payment_page.submit_payment(False)
        payment_page.qiwi_set_phone("+70")
        proceed_page = payment_page.qiwi_submit(True)
        is_error = payment_page.is_error_qiwi_phone()
        self.assertTrue(is_error, "Должна быть ошибка в форме ввода телефона")
        payment_page.qiwi_close()

        # корректный телефон qiwi
        payment_page.submit_payment(False)
        payment_page.qiwi_set_phone("+79271591181")
        proceed_page = payment_page.qiwi_submit()
        result_text = proceed_page.get_message_result()
        print(result_text)
        payment_page = proceed_page.goto_forvard()
        '''

        time.sleep(7)
        self.assertTrue(True, 'all ok')

    def test_ibit_login_negativ(self):
        """авторизация тестовыми негативными наборами тест пользователей"""
        login_page = Login_Page(selenium_driver=self.driver)
        error = login_page.login("username4@name.ru", "123456")
        self.assertEqual(error, 'Wrong password, try again', 'Ожидалась ошибка авторизации')

    def test_forgot_pass(self):
        """тесты по восстановлению пароля"""
        login_page = Login_Page(selenium_driver=self.driver)
        login_page.expand_forgot_pass()
        login_page.set_forgot_email("ru@ru.ru")
        login_page.submit_forgot()
        text = login_page.get_message()
        self.assertEqual(text, "New password was send to your email address", "Ожидаем определенное сообщение")

    @unittest.SkipTest
    def test_switch_language(self):
        """изменить язык - попробовать атворизоваться"""


def suite():
    suite1 = unittest.TestSuite()
    suite1.addTest(LoginTest.test_ibit_login("chrome"))
    return suite1


if __name__ == '__main__':
    unittest.main()
    # unittest.TextTestRunner(verbosity=2).run(suite())
