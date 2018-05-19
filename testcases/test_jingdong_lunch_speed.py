#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

from performancebasetest.launch_speed_test import LaunchSpeedTest

class JingdongLaunchSpeedTest(LaunchSpeedTest):

    """
    测试京东启动速度
    """

    def __init__(self, device_serial):
        self.case_chinese_name  = "京东冷启动测试"
        self.package_name = "com.jingdong.app.mall"
        self.activity_name = ".main.MainActivity"
        self.device_serial = device_serial
        super(JingdongLaunchSpeedTest, self).__init__(self.package_name, self.activity_name, self.device_serial, self.case_chinese_name)

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
    jingdong_launch_speed_test = JingdongLaunchSpeedTest("KFZH89MZ5LQ8YLDA")
    jingdong_launch_speed_test.test()