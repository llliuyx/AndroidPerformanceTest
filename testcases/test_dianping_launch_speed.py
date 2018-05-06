#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

from performancebasetest.launch_speed_test import LaunchSpeedTest

class DianpingLaunchSpeedTest(LaunchSpeedTest):

    """
    测试点评启动速度
    """

    def __init__(self, device_serial):
        self.case_chinese_name = "冷启动测试"
        self.package_name = "com.dianping.v1"
        self.activity_name = ".NovaMainActivity"
        self.device_serial = device_serial
        super(DianpingLaunchSpeedTest, self).__init__(self.package_name, self.activity_name, self.device_serial, self.case_chinese_name)

    def set_up(self):
        self.robot.stop_app()

    def test(self):
        for i in xrange(10):
            self.robot.start_app()
            time.sleep(5)
            self.robot.stop_app()

    def tear_down(self):
        self.robot.stop_app()


if __name__ == '__main__':
    meituan_launch_speed_test = DianpingLaunchSpeedTest("KFZH89MZ5LQ8YLDA")
    meituan_launch_speed_test.test()