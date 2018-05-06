#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.test_suite import PerformanceTestSuite
from phone.oppo_r7 import oppo
import time

class MeituanTestSuite(PerformanceTestSuite):
    def __init__(self, device_serial):
        self.app_name = "美团"
        self.package_name = "com.sankuai.meituan"
        self.activity_name = "com.meituan.android.pt.homepage.activity.MainActivity"
        self.device_serial = device_serial

        super(MeituanTestSuite, self).__init__(self.package_name, self.activity_name, self.device_serial, self.app_name)

    def suite_set_up(self):
        device = self.robot.device
        self.robot.clear_app()
        oppo.trust_app(self.app_name)
        time.sleep(.5)
        self.robot.start_app()
        time.sleep(5)
        meituan_home_page = device(resourceId="com.sankuai.meituan:id/headerContent",className="android.widget.LinearLayout")
        assert meituan_home_page.exists,"%s suite失败" % self.app_name
        self.robot.stop_app()

    def suite_tear_down(self):
        self.robot.stop_app()


if __name__ == '__main__':
    meituan_test_suite = MeituanTestSuite("KFZH89MZ5LQ8YLDA")
    meituan_test_suite.suite_set_up()