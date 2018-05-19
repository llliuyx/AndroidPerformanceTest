#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.memory_usage_test import MemoryUsageTest
from time import sleep

class MeituanMemoryUsageTest(MemoryUsageTest):

    """
    测试美团CPU消耗
    """

    def __init__(self, device_serial):
        self.case_chinese_name = "内存测试"
        self.package_name = "com.sankuai.meituan"
        self.activity_name = "com.meituan.android.pt.homepage.activity.MainActivity"
        self.device_serial = device_serial
        super(MeituanMemoryUsageTest, self).__init__(self.package_name, self.activity_name, self.device_serial, self.case_chinese_name)

    def set_up(self):
        self.robot.start_app()
        self.robot.sleep(5)
        self.robot.device.press.home()

    def test(self):
        for i in xrange(10):
            self.robot.start_app()
            self.robot.sleep(2)
            self.robot.device.press.home()
            sleep(1)

    def tear_down(self):
        self.robot.stop_app()

if __name__ == '__main__':
    meituan_memory_usage_test = MeituanMemoryUsageTest("005e0f760804")
    meituan_memory_usage_test.set_up()
    meituan_memory_usage_test.test()
