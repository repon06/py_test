#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class RegExHelper():
    ""

    def __init__(self):
        ""

    def get_digital(self, str):
        val = next(re.finditer(r'(\d+)', str)).group(0)
        return val
