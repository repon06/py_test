#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from page.Base_Page import Base_Page
from utils.RegExHelper import RegExHelper
from selenium.webdriver.support import expected_conditions as EC

from utils.WaitConditions import element_has_attribute


class Payment_Page(Base_Page):
    "страница пополнения баланса"
    page_name = "страница пополнения счета"

    # Форма позволяет выбрать сумму пополнения, валюту и платежную систему. Можно
    # взять/выключить бонус за пополнение. В соответствии с суммой пополнения
    # пользователь получает различные статусы: Mini, Silver, Gold, VIP. Есть описание
    # привелегий статусов и условия бонусной программы.

    def start(self):
        # ссылка + текст
        self.goto_status_description = 'div.header>a'

        # states
        self.states_vip = "//div[status-item[@name='vip']]"
        self.states_gold = "//div[status-item[@name='gold']]"
        self.state_silver = "//div[status-item[@name='silver']]"
        self.state_mini = "//div[status-item[@name='mini']]"
        self.status_item = ".//status-selector //div[@class='item-holder' and status-item[@name='%s']]"
        # переделать! для каждого
        self.state_get_active = "//div[status-item[@name='mini']]/status-item/div"

        # Choose payment system
        self.paym_system_select = "div.payment-system-selector div.select"
        # self.paym_system_ul_ = "//span[text()='VISA, MasterCard, Maestro']" #поиск по тексту (есть ошибка)
        self.paym_system_ul = "div.payment-system-selector ul>li>span.title"
        self.paym_system_select_img = "div.payment-system-selector div.select div[name='selectfield'] span.image"
        self.paym_system_select_title = "div.payment-system-selector div.select div[name='selectfield'] span.title"
        self.paym_system_field = "payment-system-selector div.current"
        self.sub_paym_system_field = "payment-system-selector ul.menu>li"
        self.sub_paym_system_ul = "payment-system-selector ul.menu"
        # Choose amount
        self.amount = "input[name='amount']"

        # Choose currency
        self.curr_select = "div.currency div.select"
        self.curr_ul = "//span[text()='₽ RUB']"  # поиск по тексту
        self.curr_select_title = "div.currency div.select div[name='selectfield'] span.title"
        self.currency_field = "amount-inputs div.current"
        self.sub_currency_field = "amount-inputs ul.menu>li"

        # bonus
        self.isBonus = "input#bonus-activator"
        self.bonus_value = "div.bonus div.value"

        # you get
        self.youget = "div.you-get>div.value"

        # submit - кнопка proceed
        self.submit = 'div#riot-app submit>div.submit>a>span'

        # qiwi panel
        self.qiwi_panel = "phone>div>div"
        self.sub_qiwi_phone = "input"
        self.sub_qiwi_close = "div.back>a"
        self.sub_qiwi_submit = "submit>div.submit>a>span"
        self.sub_qiwi_country_field = "rg-select div.current"
        self.sub_qiwi_sub_country_fields = "ul.menu>li"

        # ждем загрузки стр
        self.wait_page_load(By.CSS_SELECTOR, self.goto_status_description)

    def is_PaymentPage(self):
        '''проверяем нужная ли нам страница'''
        return self.driver.find_element(By.CSS_SELECTOR, self.submit).is_enabled()

    def goto_pricing(self):
        self.driver.find_element(By.CSS_SELECTOR, self.goto_status_description).click()
        from page.Pricing_Page import Pricing_Page
        return Pricing_Page(selenium_driver=self.driver)

    # STATUS
    def select_status(self, stat):
        self.driver.find_element(By.XPATH, self.status_item % stat).click()
        # ждем изменения актульн стат
        wait = WebDriverWait(self.driver, 15)
        wait.until(element_has_attribute(By.CSS_SELECTOR, "div.status-selector>div>status-item", "active"), stat)

    def get_active_status(self):
        element = self.driver.find_elements(By.CSS_SELECTOR, "div.status-selector>div>status-item")[
            0]  # всего 4 элемента
        active_status = element.get_attribute("active")
        return active_status

    def select_payment_system(self, value):
        self.select_of_webelement(By.CSS_SELECTOR, self.paym_system_field, self.sub_paym_system_field, value)

    # BONUS
    def get_state_bonus(self):
        return self.driver.find_element_by_css_selector(self.isBonus).is_selected()  # checked

    def check_bonus(self):
        # self.script_edit_css_property(self.isBonus, 'visibility', 'visible')
        # self.script_edit_css_property(self.isBonus, 'opacity', 1)

        element = self.driver.find_element(By.CSS_SELECTOR, self.isBonus)
        self.click_script(element)

    def get_bonus_value(self):
        element = self.driver.find_element(By.CSS_SELECTOR, self.bonus_value)
        text = element.text
        digital = RegExHelper().get_digital(text)
        return digital

    def get_you_get(self):
        element = self.driver.find_element(By.CSS_SELECTOR, self.youget)
        digital = RegExHelper().get_digital(element.text)
        return digital

    # AMOUNT
    def get_amount_value(self):
        element = self.driver.find_element(By.CSS_SELECTOR, self.amount)
        return element.get_attribute("value")

    def set_amount_value(self, value):
        element = self.driver.find_element(By.CSS_SELECTOR, self.amount)
        element.clear()
        element.send_keys(value)

    def select_currency(self, value):
        self.select_of_webelement(By.CSS_SELECTOR, self.currency_field, self.sub_currency_field, value)
        '''
        element = self.driver.find_element(By.CSS_SELECTOR, self.currency_field ) #div.field
        element.click()

        #sub_elements = self.driver.find_elements(By.XPATH, ".//amount-inputs //ul/li[span[contains(text(),'CNH')]]") #(By.CSS_SELECTOR, "amount-inputs ul.menu>li")
        sub_elements = self.driver.find_elements(By.CSS_SELECTOR, "amount-inputs ul.menu>li")
        if len(sub_elements)>0:
            for item in sub_elements:
                print(item.text)
                if value in item.text:
                    item.click()
        '''

    def get_value_currency(self):
        element = self.driver.find_element(By.CSS_SELECTOR, self.currency_field)
        return element.text

    def get_value_payment_system(self):
        element = self.driver.find_element(By.CSS_SELECTOR, self.paym_system_field)
        return element.text

    def get_indicator_discription(self):
        """нижний индикатор - бегунок с описанием - реализовать"""
        return ""

    # submit_proces
    def submit_payment(self, is_final: bool = True):
        """запустить процесс по оплате, is_final - возвращаем ли страницу"""
        self.driver.find_element(By.CSS_SELECTOR, self.submit).click()
        if is_final:
            from page.Processed_Page import Processed_Page
            return Processed_Page(selenium_driver=self.driver)

    def is_qiwi_visible(self):
        elems = self.driver.find_elements(By.CSS_SELECTOR, self.qiwi_panel)
        return len(elems) > 0 and elems[0].is_displayed()

    def qiwi_set_phone(self, value):
        panel = self.driver.find_element(By.CSS_SELECTOR, self.qiwi_panel)
        panel.find_element(By.CSS_SELECTOR, self.sub_qiwi_phone).send_keys(value)

    def is_error_qiwi_phone(self):
        panel = self.driver.find_element(By.CSS_SELECTOR, self.qiwi_panel)
        error_class = panel.find_element(By.CSS_SELECTOR, self.sub_qiwi_phone).get_attribute("class")
        # print(error_class)
        return "error" in error_class

    def qiwi_submit(self, is_error: bool = False):
        panel = self.driver.find_element(By.CSS_SELECTOR, self.qiwi_panel)
        panel.find_element(By.CSS_SELECTOR, self.sub_qiwi_submit).click()
        if is_error == False:
            from page.Processed_Page import Processed_Page
            return Processed_Page(selenium_driver=self.driver)

    def qiwi_close(self):
        panel = self.driver.find_element(By.CSS_SELECTOR, self.qiwi_panel)
        panel.find_element(By.CSS_SELECTOR, self.sub_qiwi_close).click()
