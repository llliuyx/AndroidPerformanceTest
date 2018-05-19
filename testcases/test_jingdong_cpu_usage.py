#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.cpu_usage_test import CPUUsageTest
import time


class JingdongCPUUsageest(CPUUsageTest):

    """
    测试京东CPU消耗
    """

    def __init__(self,device_serial):
        self.case_chinese_name = "京东CPU消耗测试"
        self.package_name = "com.jingdong.app.mall"
        self.activity_name = ".main.MainActivity"
        self.device_serial = device_serial
        super(JingdongCPUUsageest, self).__init__(self.package_name, self.activity_name, self.device_serial, self.case_chinese_name )

    def set_up(self):
        self.robot.start_app()
        # time.sleep(5)

    def test(self):
        for i in xrange(10):
            self.robot.device.swipe(520, 1460, 520, 400)
            time.sleep(1)

    def tear_down(self):
        self.robot.stop_app()



if __name__ == '__main__':
    jingdong_cpu_usage_test = JingdongCPUUsageest("KFZH89MZ5LQ8YLDA")
    jingdong_cpu_usage_test.test()