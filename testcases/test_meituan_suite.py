#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.test_suite import PerformanceTestSuite
import time

class MeituanTestSuite(PerformanceTestSuite):
    def __init__(self):
        self.package_name = "com.sankuai.meituan"
        self.activity_name = ".activity.MainActivity"
        self.device_serial = "QMSDU15C14012513"

        super(MeituanTestSuite, self).__init__(self.package_name, self.activity_name, self.device_serial)

    def suite_set_up(self):
        device = self.robot.device
        self.robot.clear_app()
        self.robot.start_app()

        privilege_enable_btn = device(className="android.widget.Button", text="始终允许")
        redbag_popup = device(resourceId="com.sankuai.meituan:id/start_pop_close")
        while privilege_enable_btn.exists:
            print "click privilage"
            privilege_enable_btn.click()
            time.sleep(.5)

        for i in xrange(10):
            if redbag_popup.exists:
                redbag_popup.click()
                break
            time.sleep(1)

        self.robot.stop_app()

    def suite_tear_down(self):
        print "=======meituan suite_tear_down========="
        pass


if __name__ == '__main__':
    meituan_test_suite = MeituanTestSuite("com.sankuai.meituan", ".activity.MainActivity", "QMSDU15C14012513")
    meituan_test_suite.suite_set_up()