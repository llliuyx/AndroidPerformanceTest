#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.launch_speed_test import LaunchSpeedTest

class MeituanLaunchSpeedTest(LaunchSpeedTest):
    """
    测试美团启动速度
    """

    def __init__(self, package_name, activity_name, device_serial):
        super(MeituanLaunchSpeedTest, self).__init__(package_name, activity_name, device_serial)

    def test(self):
        self.robot.stop_app()

        for i in xrange(10):
            self.robot.start_app()

            self.robot.stop_app()



if __name__ == '__main__':
    meituan_launch_speed_test = MeituanLaunchSpeedTest("com.sankuai.meituan", ".activity.MainActivity", "DLQ0216901001320")
    meituan_launch_speed_test.test()