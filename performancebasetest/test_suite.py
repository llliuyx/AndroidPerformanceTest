#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
from utils.robot import Robot

class PerformanceTestSuite(object):
    __metaclass__ = ABCMeta

    def __init__(self, package_name, activity_name, device_serial):
        self.package_name = package_name
        self.activity_name = activity_name
        self.device_serial = device_serial
        self.robot = Robot(self.package_name, self.activity_name, self.device_serial)

    @abstractmethod
    def suite_set_up(self):
        pass

    @abstractmethod
    def suite_tear_down(self):
        pass