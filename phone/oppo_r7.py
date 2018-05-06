#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
from utils.robot import Robot

class Oppo():

    def __init__(self, package_name, activity_name, device_serial):
        self.package_name = package_name
        self.activity_name = activity_name
        self.device_serial = device_serial
        self.robot = Robot(self.package_name, self.activity_name, self.device_serial)
        # self.robot.start_app(self.package_name, self.activity_name)

    def trust_app(self,app_ame):
        device = self.robot.device
        self.robot.start_app(pkg_name="com.color.safecenter", activity_name=".permission.PermissionManagerActivity")
        time.sleep(3)
        # 打开权限
        # safty = device(text = "安全中心")
        # safty.click()
        # permissions_privacy = device(text="权限隐私")
        # permissions_privacy.click()
        # time.sleep(.5)
        # application_manager = device(text="应用权限管理")
        # application_manager.click()
        device(text="按应用程序管理").click()
        device(className="android.widget.ListView", resourceId="android:id/list") \
            .child_by_text(app_ame, allow_scroll_search=True, resourceId="android:id/title") \
            .click()
        check_button = device(resourceId="android:id/checkbox", checked="false")
        if check_button.exists:
            check_button.click()

        self.robot.stop_app(pkg_name="com.color.safecenter")

oppo = Oppo("com.dianping.v1", "com.dianping.main.guide.SplashScreenActivity","KFZH89MZ5LQ8YLDA")
