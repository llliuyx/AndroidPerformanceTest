#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.test_case import PerformanceTestCase
import threading
import time

class CPUUsageTest(PerformanceTestCase):
    """
    CPU耗时测试基础类
    """
    def __init__(self, package_name, activity_name, device_serial, log=None):
        super(CPUUsageTest, self).__init__(package_name, activity_name, device_serial, log)
        self.is_finished = False
        self.__jiffs_list = []
        self.pid = self.adb_tools.get_pid(self.package_name)
        self.is_first = True

    def set_up(self):
        self.timer = threading.Timer(1, self.__fun_get_jiffs)
        self.timer.start()

    def test(self):
        pass

    def tear_down(self):
        print self.__jiffs_list
        pass

    def __fun_get_jiffs(self):
        self.timer = threading.Timer(5, self.__fun_get_jiffs)
        self.timer.start()
        current_timestamp = time.time()
        utime, stime = self.__get_jiffs()

        if self.is_first:
            self.is_first = False
            self.__start_jiffs_item = JiffsUnit(current_timestamp, utime, stime)
            self.__last_utime = utime
            self.__last_stime = stime
        elif utime > 0 and stime > 0:
            u = utime - self.__last_utime
            s = stime - self.__last_stime
            jiffs_unit = JiffsUnit(current_timestamp, u, s)
            jiffs_string = jiffs_unit.__str__()
            print jiffs_string
            # self.log.info(jiffs_string)
            self.__jiffs_list.append(jiffs_unit)
            self.__last_utime = utime
            self.__last_stime = stime

    def __get_jiffs(self):
        output = self.adb_tools.shell("cat /proc/%s/stat" % self.pid).read()
        # print output
        if not output:
            return -1, -1
        # self.log.info(output)
        list_output = output.split()
        try:
            utime = int(list_output[13])
            stime = int(list_output[14])
        except Exception:
            utime = -1
            stime = -1

        return utime, stime

class JiffsUnit(object):
    def __init__(self, timestamp, utime, stime):
        self.timestamp = timestamp
        self.utime = utime
        self.stime = stime

    def __str__(self):
        return "%s, utime: %s, stime: %s" %(self.format_time(), str(self.utime), str(self.stime))

    def format_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))


if __name__ == '__main__':
    cpu_usage_test = CPUUsageTest("com.sankuai.meituan", ".activity.MainActivity", "005e0f760804")
    cpu_usage_test.set_up()