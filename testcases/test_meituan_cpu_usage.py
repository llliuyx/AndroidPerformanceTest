#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.cpu_usage_test import CPUUsageTest
from time import sleep

class MeituanCPUUsageest(CPUUsageTest):

    """
    测试美团启动速度
    """

    def __init__(self):
        self.package_name = "com.sankuai.meituan"
        self.activity_name = ".activity.MainActivity"
        self.device_serial = "QMSDU15C14012513"
        super(MeituanCPUUsageest, self).__init__(self.package_name, self.activity_name, self.device_serial)

    def test(self):
        # print "MeituanCPUUsageest, 待实现"
        self.robot.start_app()
        for i in xrange(10):
            self.robot.device.swipe(520, 1460, 520, 400)
            sleep(1)



if __name__ == '__main__':
    meituan_cpu_usage_test = MeituanCPUUsageest()
    meituan_cpu_usage_test.test()