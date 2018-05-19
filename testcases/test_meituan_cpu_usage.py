#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.cpu_usage_test import CPUUsageTest
from time import sleep
import time

class MeituanCPUUsageTest(CPUUsageTest):

    """
    测试美团CPU消耗
    """

    def __init__(self, device_serial):
        self.case_chinese_name = "CPU消耗测试"
        self.package_name = "com.sankuai.meituan"
        self.activity_name = "com.meituan.android.pt.homepage.activity.MainActivity"
        self.device_serial = device_serial
        super(MeituanCPUUsageTest, self).__init__(self.package_name, self.activity_name, self.device_serial, self.case_chinese_name)

    def set_up(self):
        self.robot.start_app()
        # time.sleep(5)

    def test(self):
        for i in xrange(10):
            self.robot.device.swipe(520, 1460, 520, 400)
            sleep(1)

    def tear_down(self):
        self.robot.stop_app()

if __name__ == '__main__':
    meituan_cpu_usage_test = MeituanCPUUsageTest("KFZH89MZ5LQ8YLDA")
    meituan_cpu_usage_test.test()