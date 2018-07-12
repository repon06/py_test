#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from page.Base_Page import Base_Page
from selenium.webdriver.support import expected_conditions as EC


class Login_Page(Base_Page):
    "страница авторизации"
    page_name = "страница авторизации"

    def start(self):
        self.url = ""
        self.open(self.url)
        # self.assertIn("ExpertOption billing test", self.driver.title)

        # language
        self.language_en = "div.en>a"
        self.language_ch = "div.zh>a"
        self.language_ko = "div.ko>a"
        self.language_ru = "div.ru>a"
        self.language_hi = "div.hi>a"

        # login
        self.login_email = "//input[@name='username']"
        self.login_pass = "//textarea[@name='password']"
        self.login_submit = "//div[@class='submit gold']"  # /a"

        # forgot pass
        self.forgot_pass_button = "a.forgot"
        self.forgot_pass_email = "//input[@name='forgotPass']"
        self.forgot_pass_submit = "button.submit"  # "button[class='submit gold']"

        # ждем загрузки стр
        self.wait_page_load(By.XPATH, self.login_submit)

    def login(self, username, password):
        self.set_login_email(username)
        self.set_login_pass(password)
        self.submit_login()
        # from utils.PageFactory import PageFactory
        # return PageFactory().getPageObject("payment page", self.driver)

        err_msg = self.get_message()
        if err_msg != None:
            self.close_message()
            return err_msg

        from page.Payment_Page import Payment_Page
        return Payment_Page(selenium_driver=self.driver)

    def set_login_email(self, username):
        self.driver.find_element(By.XPATH, self.login_email).send_keys(username)

    def set_login_pass(self, password):
        self.driver.find_element(By.XPATH, self.login_pass).send_keys(password)

    def submit_login(self):
        self.driver.find_element(By.XPATH, self.login_submit).click()

    def select_language(self, lang):
        """выбор языка интерфейса"""
        # self.driver.find_elements(By.CSS_SELECTOR,self.forgot_pass_button)

    def expand_forgot_pass(self):
        self.driver.find_element(By.CSS_SELECTOR, self.forgot_pass_button).click()
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.forgot_pass_submit)))

    def is_forgot_visible(self):
        element = self.driver.find_element(By.XPATH, self.forgot_pass_email)
        return element.is_displayed()

    def set_forgot_email(self, value):
        if self.is_forgot_visible():
            element = self.driver.find_element(By.XPATH, self.forgot_pass_email)
            element.clear()
            element.send_keys(value)

    def submit_forgot(self):
        self.driver.find_element(By.CSS_SELECTOR, self.forgot_pass_submit).click()
