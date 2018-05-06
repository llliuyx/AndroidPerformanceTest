#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
from utils.robot import Robot
from utils.adbtools import AdbTools
from utils.log_handler import get_logger


class PerformanceTestCase(object):
    __metaclass__ = ABCMeta

    def __init__(self, package_name, activity_name, device_serial, case_chinese_name, log=None):
        self.case_chinese_name = case_chinese_name
        self.package_name = package_name
        self.activity_name = activity_name
        self.device_serial = device_serial
        self.robot = Robot(package_name, activity_name, device_serial)
        self.adb_tools = AdbTools(self.device_serial)
        self.log = log

    @abstractmethod
    def set_up(self):
        pass

    @abstractmethod
    def tear_down(self):
        pass

    @abstractmethod
    def test(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def end(self):
        pass

    @abstractmethod
    def results(self):
        pass