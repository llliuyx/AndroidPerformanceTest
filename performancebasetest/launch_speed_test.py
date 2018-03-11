#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import threading
import re
from utils.Adb import Adb
from utils.robot import Robot

class LaunchSpeedTest(object):
    """
    启动时间测试基础类
    """
    def __init__(self, package_name, activity_name, device_serial):
        self.package_name = package_name
        self.activity_name = activity_name
        self.device_serial = device_serial
        self.is_finished = False
        self.__launch_speed_list = []
        self.robot = Robot(package_name, activity_name, device_serial)

    def set_up(self):
        self.exec_logcat()
        self.start_collect_data()

    def test(self):
        pass

    def tear_down(self):
        pass

    def exec_logcat(self):
        logcat_cmd = "logcat -v time ActivityManager:I *:S"
        logcat_popen = Adb.exec_shell_cmd(self.device_serial, logcat_cmd)
        self.logcat_stdout = logcat_popen.stdout

    def read_logcat_stdout(self):
        return self.logcat_stdout.readline()

    def start_collect_data(self):
        self.launch_speed_collect_thread = threading.Thread(target=self.__collect_data, name="launch_speed_collect_thread")
        self.launch_speed_collect_thread.start()

    # def finish_collect_data(self):
        # self.launch_speed_collect_thread.join()

    def __collect_data(self, thread_name="launch_speed_collect_thread"):
        print "start the thread: ", thread_name
        DISPLAYE_TAG = "Displayed"

        def get_launch_speed_from_line(log_line):
            """
            :param log_line:
            :return: launch speed (ms)
            """
            if log_line.find('total') > 0:
                s1 = re.findall("total\\s\\+(\\w+)ms", log_line)[0]
            else:
                s1 = re.findall("\+(\\w+)ms", log_line)[0]

            if s1.find('s') > 0:
                s2 = s1.split('s')
                s3 = int(s2[0]) * 1000 + int(s2[1])
                return s3
            else:
                return s1

        while not self.is_finished:
            line = self.read_logcat_stdout()
            if DISPLAYE_TAG not in line:
                continue
            if self.package_name not in line:
                continue
            if self.activity_name not in line:
                continue
            print line

            print get_launch_speed_from_line(line)
            self.__launch_speed_list.append(get_launch_speed_from_line(line))


if __name__ == '__main__':
    launchSpeed = LaunchSpeedTest("com.sankuai.meituan", ".activity.MainActivity", "DLQ0216901001320")
    launchSpeed.exec_logcat()
    launchSpeed.start_collect_data()