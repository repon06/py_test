#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import urllib  # 2.7 import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils.ConfigHelper import ConfigHelper


class Base_Page(object):  # unittest.TestCase
    "базовый класс страниц"

    def __init__(self, selenium_driver: WebDriver, base_url='https://ibitcy.com/interview/qa/mobile-deposit/'):

        # notifications
        self.notification = "div.notification"
        self.notification_message = "div.text"  # "div.notification>div.text"
        self.notification_close = "div.close"  # "div.notification>div.close"

        # logger object
        logging.basicConfig(filename="ibit.log", level=logging.INFO)
        self.log_obj = logging.getLogger('ibit')

        self.base_url = base_url
        self.driver = selenium_driver
        self.driver.implicitly_wait(0)
        self.driver.maximize_window()
        self.start()

    def open(self, url=""):
        url = self.base_url + url
        if self.base_url not in self.driver.current_url:
            basic_auth_user = ConfigHelper().getConfigOption('base_auth', 'basic_auth_user')
            basic_auth_pass = ConfigHelper().getConfigOption('base_auth', 'basic_auth_pass')
            urlpars = urllib.parse.urlsplit(url)  # urlparse.urlparse(url)
            url = urlpars.scheme + "://%s:%s@" % (basic_auth_user, basic_auth_pass) + urlpars.netloc + urlpars.path

        self.driver.get(url)

    def click_script(self, element: WebElement):
        """клик по hidden элементу"""
        self.driver.execute_script("arguments[0].click();", element)

    def script_edit_css_property(self, selector, prop_name, value):
        """изменить св-во элта скриптом"""
        js = "document.querySelector('{0}').style.{1}='{2}'".format(selector, prop_name, value)
        self.driver.execute_script(js);
        # self.driver.execute_script("document.querySelector('input#bonus-activator').style.visibility='visible'");
        # self.driver.execute_script("document.querySelector('input#bonus-activator').style.opacity='1'");

    def write(self, msg, level='INFO'):
        self.log_obj.debug(msg, level)

    def wait(self, wait_seconds=5):
        time.sleep(wait_seconds)

    def wait_page_load(self, by, selector):
        """ожидаем загрузки страницы"""
        # try:
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.element_to_be_clickable((by, selector)))
        self.write('Страница %s загружена' % self.page_name)
        # except TimeoutException:
        #    self.write('Не дождались появления элемента!')
        # except Exception as e:
        #    self.write('Ошибка при ожидании загрузки страницы: %s' % e.message)

    def get_message(self):
        """если находим, возвращаем элемент сообщения"""
        elements = self.driver.find_elements_by_css_selector(self.notification)
        if len(elements) > 0:
            text = elements[0].find_element(By.CSS_SELECTOR, self.notification_message).text
            return text
        else:
            self.write("no found error msg")

        return None

    def close_message(self):
        """если находим, возвращаем элемент сообщения"""
        elements = self.driver.find_elements_by_css_selector(self.notification)
        if len(elements) > 0:
            elements[0].find_element(By.CSS_SELECTOR, self.notification_close).click()
            # WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(By.CSS_SELECTOR, self.notification))

    def select_of_webelement(self, by, select, sub_select, value):
        element = self.driver.find_element(by, select)  # div.field
        element.click()

        sub_elements = self.driver.find_elements(by, sub_select)
        if len(sub_elements) > 0:
            for item in sub_elements:
                # print(item.text)
                if value in item.text:
                    item.click()
                    # ждем исчезновения
                    wait = WebDriverWait(self.driver, 15)
                    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, sub_select)))
                    return
