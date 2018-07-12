#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from page.Base_Page import Base_Page


class Pricing_Page(Base_Page):
    "страница описания привелегий"
    page_name = "страница описания привелеги"

    def start(self):
        self.button_close = "div.btn-close"
        self.header = "div.pricing div.text"

        # ждем загрузки стр
        self.wait_page_load(By.CSS_SELECTOR, self.button_close)

    def get_header(self):
        elem = self.driver.find_element(By.CSS_SELECTOR, self.header)
        return elem.text

    def goto_payment(self):
        self.driver.find_element(By.CSS_SELECTOR, self.button_close).click()
        from page.Payment_Page import Payment_Page
        return Payment_Page(selenium_driver=self.driver)
