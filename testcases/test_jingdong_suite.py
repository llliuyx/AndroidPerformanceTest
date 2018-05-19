#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.test_suite import PerformanceTestSuite
from phone.oppo_r7 import oppo
import time

class JingdongTestSuite(PerformanceTestSuite):
    def __init__(self, device_serial):
        self.app_name = "京东"
        self.package_name = "com.jingdong.app.mall"
        self.activity_name = ".main.MainActivity"
        self.device_serial = device_serial
        super(JingdongTestSuite, self).__init__(self.package_name, self.activity_name, self.device_serial, self.app_name)

    def suite_set_up(self):
        device = self.robot.device
        self.robot.clear_app()
        # 应用授权
        oppo.trust_app("京东")
        # 启动App
        self.robot.start_app()
        time.sleep(5)
        privacy = device(text="同意")
        if privacy.exists:
            privacy.click()
        time.sleep(5)
        lunch_page = device(resourceId="com.jingdong.app.mall:id/c_7", className="android.widget.ImageView")
        if lunch_page.exists:
            lunch_page.click()
        # time.sleep(5)
        # 红包弹窗
        red_bag_popup = device(resourceId="com.jingdong.app.mall:id/l2", className="android.widget.ImageView")
        if red_bag_popup.exists:
            red_bag_popup.click()
        homepage_flag = device(resourceId="com.jingdong.app.mall:id/ha", className="android.support.v4.view.ViewPager")
        assert homepage_flag.exists, "%s Suite失败." % self.app_name
        self.robot.stop_app()

    def suite_tear_down(self):
        self.robot.stop_app()


if __name__ == '__main__':
    jingdong_test_suite = JingdongTestSuite("KFZH89MZ5LQ8YLDA")
    jingdong_test_suite.suite_set_up()