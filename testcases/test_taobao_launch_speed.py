#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time

from performancebasetest.launch_speed_test import LaunchSpeedTest

class TaobaoLaunchSpeedTest(LaunchSpeedTest):

    """
    测试淘宝启动速度
    """

    def __init__(self, device_serial):
        self.case_chinese_name = "淘宝冷启动测试"
        self.package_name = "com.taobao.taobao"
        self.activity_name = "com.taobao.tao.homepage.MainActivity3"
        self.device_serial = device_serial
        super(TaobaoLaunchSpeedTest, self).__init__(self.package_name, self.activity_name, self.device_serial, self.case_chinese_name )

    def set_up(self):
        self.robot.stop_app()
        time.sleep(5)

    def test(self):
        self.robot.stop_app()

        for i in xrange(10):
            self.robot.start_app()
            time.sleep(5)
            self.robot.stop_app()

    def tear_down(self):
        self.robot.stop_app()

if __name__ == '__main__':
    taobao_launch_speed_test = TaobaoLaunchSpeedTest("KFZH89MZ5LQ8YLDA")
    taobao_launch_speed_test.test()

