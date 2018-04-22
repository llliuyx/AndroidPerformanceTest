#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.launch_speed_test import LaunchSpeedTest

class MeituanLaunchSpeedTest(LaunchSpeedTest):

    """
    测试美团启动速度
    """

    def __init__(self):
        self.package_name = "com.sankuai.meituan"
        self.activity_name = ".activity.MainActivity"
        self.device_serial = "QMSDU15C14012513"
        super(MeituanLaunchSpeedTest, self).__init__(self.package_name, self.activity_name, self.device_serial)

    def test(self):
        self.robot.stop_app()

        for i in xrange(10):
            self.robot.start_app()

            self.robot.stop_app()


if __name__ == '__main__':
    meituan_launch_speed_test = MeituanLaunchSpeedTest()
    meituan_launch_speed_test.test()