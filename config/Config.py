#! /usr/bin/env python
# -*- coding: UTF-8 -*-


import yaml
import logging
import os
import json
# env = "DEBUG"1


class Log(object):
    def __init__(self, name, level="DEBUG"):
        self.logger = logging.getLogger(name)
        if level == "CRITICAL":
            self.logger.setLevel(logging.CRITICAL)
        elif level == "ERROR":
            self.logger.setLevel(logging.ERROR)
        elif level == "WARNING":
            self.logger.setLevel(logging.WARNING)
        elif level == "INFO":
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        current_path = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(current_path + "/log"):
            os.makedirs(current_path + "/log")
        fh = logging.FileHandler(filename=current_path + '/log/%s.log' % name, mode='w', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(filename)s - line:%(lineno)d - %(name)s - '
                                      '%(levelname)s - %(funcName)s() -  %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)


class Config(object):
    L = Log('Config')

    def __init__(self, name, current_path=None):
        self.name = name
        if current_path is None:
            current_path = os.path.dirname(os.path.abspath(__file__))
        with open(current_path + "/" + name + ".yaml", encoding='utf-8') as f:
            self.data = yaml.safe_load(f)
