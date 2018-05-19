#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.traffic_usage_test import TrafficUsageTest
from time import sleep

class MeituanTrafficUsageTest(TrafficUsageTest):
    """
    美团首页滑动流量测试
    """

    def __init__(self, device_serial):
        self.case_chinese_name = "美团首页滑动流量测试"
        self.package_name = "com.sankuai.meituan"
        self.activity_name = "com.meituan.android.pt.homepage.activity.MainActivity"
        self.device_serial = device_serial
        super(MeituanTrafficUsageTest, self).__init__(self.package_name, self.activity_name, self.device_serial, self.case_chinese_name)

    def set_up(self):
        self.robot.stop_app()
        self.robot.start_app()
        self.robot.sleep(10)

    def test(self):
        for i in xrange(10):
            self.robot.device.swipe(520, 1460, 520, 400)
            sleep(1)
        self.robot.sleep(5 * 60)

    def tear_down(self):
        self.robot.stop_app()

if __name__ == '__main__':
    meituan_memory_usage_test = MeituanTrafficUsageTest("005e0f760804")
    meituan_memory_usage_test.set_up()
    meituan_memory_usage_test.test()