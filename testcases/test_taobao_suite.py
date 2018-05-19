#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.test_suite import PerformanceTestSuite
from phone.oppo_r7 import oppo
import time

class TaobaoTestSuite(PerformanceTestSuite):
    def __init__(self,device_serial):
        self.app_name = "淘宝"
        self.package_name = "com.taobao.taobao"
        self.activity_name = "com.taobao.tao.homepage.MainActivity3"
        self.device_serial = device_serial
        super(TaobaoTestSuite, self).__init__(self.package_name, self.activity_name, self.device_serial, self.app_name)

    def suite_set_up(self):
        device = self.robot.device
        self.robot.clear_app()
        # 应用授权
        oppo.trust_app("手机淘宝")
        # 启动App
        self.robot.start_app()
        # lunch_page = device(text="同意", resourceId="com.taobao.taobao:id/yes")
        # if lunch_page.exists:
        #     lunch_page.click()
        time.sleep(5)
        homepage_flag = device(resourceId="com.taobao.taobao:id/home_swipe_refresh", className="android.view.View")
        assert homepage_flag.exists, "%s suite失败" % self.app_name

        self.robot.stop_app()

    def suite_tear_down(self):
        self.robot.stop_app()


if __name__ == '__main__':
    taobao_test_suite = TaobaoTestSuite("KFZH89MZ5LQ8YLDA")
    taobao_test_suite.suite_set_up()