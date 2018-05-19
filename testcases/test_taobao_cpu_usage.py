#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.cpu_usage_test import CPUUsageTest
import time


class TaobaoCPUUsageest(CPUUsageTest):

    """
    测试淘宝CPU消耗
    """

    def __init__(self, device_serial):
        self.case_chinese_name = "淘宝CPU消耗测试"
        self.package_name = "com.taobao.taobao"
        self.activity_name = "com.taobao.tao.homepage.MainActivity3"
        self.device_serial = device_serial
        super(TaobaoCPUUsageest, self).__init__(self.package_name, self.activity_name, self.device_serial, self.case_chinese_name )

    def set_up(self):
        self.robot.stop_app()

    def test(self):

        self.robot.start_app()
        time.sleep(5)
        for i in xrange(10):
            self.robot.device.swipe(520, 1460, 520, 400)
            time.sleep(1)

    def tear_down(self):
        self.robot.stop_app()

if __name__ == '__main__':
    taobao_cpu_usage_test = TaobaoCPUUsageest("KFZH89MZ5LQ8YLDA")
    taobao_cpu_usage_test.test()