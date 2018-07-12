#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.remote.webdriver import WebDriver


class element_has_attribute(object):
    """
    expect element has a attribute
    locator - find element
    returns WebElement attribute
    """

    def __init__(self, by, locator, attribute):
        self.by = by
        self.locator = locator
        self.attribute = attribute

    def __call__(self, driver: WebDriver):
        elements = driver.find_elements(self.by, self.locator)
        if len(elements)>0:
            a = elements[0].get_attribute(self.attribute)
            #print(a)
            return a
        else:
             return False

# Wait until an element with id='myNewInput' has class 'myCSSClass'
# wait = WebDriverWait(driver, 10)
# element = wait.until(element_has_css_class((By.ID, 'myNewInput'), "myCSSClass"))
