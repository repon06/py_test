#!/usr/bin/env python
# -*- coding: utf-8 -*-

from page.Payment_Page import Payment_Page
from page.Login_Page import Login_Page
from page.Pricing_Page import Pricing_Page

class PageFactory():
    "инициализация элементов старниц"

    def getPageObject(page_name, driver):
        "return page object on page_name"
        page_name = page_name.lower()
        if page_name == "login page":
            test_obj = Login_Page(selenium_driver=driver)
        elif page_name == "payment page":
            test_obj = Payment_Page(selenium_driver=driver)
        elif page_name == "pricing page":
            test_obj = Pricing_Page(selenium_driver=driver)
        return test_obj

    getPageObject = staticmethod(getPageObject)