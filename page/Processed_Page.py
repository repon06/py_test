#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page.Base_Page import Base_Page


class Processed_Page(Base_Page):
    "Страница - заявка обрабатывается"
    '''
    После нажатия на кнопку “Продолжить” происходит переход на платежную систему, в
    рамках тестового задания этот переход эмулирован как страница "Ваша заявка
    обрабатывается, подождите".
    '''
    page_name = "processed page"

    def start(self):
        self.deposit_result = "div.deposit-result>h1"
        self.forvard = "div.deposit-result>div>a"

        # ожидаем загрузки
        self.wait_page_load(By.CSS_SELECTOR, self.forvard)

        '''
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(By.CSS_SELECTOR, self.deposit_result))
        except NoSuchElementException as ex:
            self.write(ex.message)
        # finally: self.driver.quit()
        '''

    def get_message_result(self):
        return self.driver.find_element_by_css_selector(self.deposit_result).text

    def goto_forvard(self):
        self.driver.find_element_by_css_selector(self.forvard).click()
        from page.Payment_Page import Payment_Page
        return Payment_Page(selenium_driver=self.driver)
