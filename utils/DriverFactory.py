#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver

'''
ChromeDriver v2.32 (2017-08-30):
Supports Chrome v59-61

ChromeDriver v2.9 (2014-01-31):
Supports Chrome v31-34

ChromeDriver v2.39 (2018-05-30):
Supports Chrome v66-68

ChromeDriver 2.40
Supports Chrome v66-68
'''

class DriverFactory():

    def __init__(self, browser = "chrome"):
        "конструктор Driver factory"
        self.browser = browser

    def get_web_driver(self, browser):
        "возвращает веб-драйвер"
        if browser.lower() == "ff" or browser.lower() == "firefox":
            driver = webdriver.Firefox()
        elif browser.lower() == "ie":
            driver = webdriver.Ie()
        elif browser.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-blink-features=BlockCredentialedSubresources')
            driver = webdriver.Chrome(chrome_options=options)
        elif browser.lower() == "opera":
            driver = webdriver.Opera()
        elif browser.lower() == "safari":
            driver = webdriver.Safari()

        return driver

