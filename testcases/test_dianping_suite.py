#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.test_suite import PerformanceTestSuite
from phone.oppo_r7 import oppo
import time

class DianpingTestSuite(PerformanceTestSuite):
    def __init__(self, device_serial):
        self.app_name = "大众点评"
        self.package_name = "com.dianping.v1"
        self.activity_name = ".NovaMainActivity"
        self.device_serial = device_serial

        super(DianpingTestSuite, self).__init__(self.package_name, self.activity_name, self.device_serial, self.app_name)

    def suite_set_up(self):
        device = self.robot.device

        oppo.trust_app(self.app_name)
        time.sleep(.5)
        self.robot.start_app()
        self.robot.stop_app()
        self.robot.start_app()
        time.sleep(5)
        homepage_flag = device(resourceId="com.dianping.v1:id/home_category_layout", className="android.support.v7.widget.RecyclerView")
        assert homepage_flag.exists, "%s Suite失败." % self.app_name

        self.robot.stop_app()

    def suite_tear_down(self):
        self.robot.stop_app()


if __name__ == '__main__':
    dianping_test_suite = DianpingTestSuite("KFZH89MZ5LQ8YLDA")
    dianping_test_suite.suite_set_up()
