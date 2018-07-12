#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import os


class ConfigHelper():
    "чтение конфига"

    def __init__(self):
        ""

    def getConfigOption(self, section, option):
        "возвращаем нужн конфиг/переменную из файла"
        accounts_file = os.path.join(os.path.dirname(__file__), 'accounts.conf')
        config = configparser.RawConfigParser()
        config.read(accounts_file)
        #login = config.get('base_auth', 'basic_auth_user')
        #passwd = config.get('base_auth', 'basic_auth_pass')
        value = config.get(section, option)
        return value