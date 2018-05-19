#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.test_case import PerformanceTestCase
import threading
import time
from abc import ABCMeta, abstractmethod

class MemoryUsageTest(PerformanceTestCase):
    """
    内存测试基础类
    """
    __metaclass__ = ABCMeta
    def __init__(self, package_name, activity_name, device_serial, case_chinese_name, log=None):
        super(MemoryUsageTest, self).__init__(package_name, activity_name, device_serial, case_chinese_name, log)
        self.is_finished = True
        self.__memory_list = []

    @abstractmethod
    def set_up(self):
        pass

    @abstractmethod
    def test(self):
        pass

    @abstractmethod
    def tear_down(self):
        pass

    @property
    def type(self):
        return "memory"

    @property
    def results(self):
        return self.__memory_list

    def start(self):
        self.timer = threading.Timer(1, self.__fun_get_memory)
        self.timer.start()

    def end(self):
        self.timer.cancel()
        print self.results

    def __fun_get_memory(self):
        self.timer = threading.Timer(3, self.__fun_get_memory)
        self.timer.start()
        timestamp = time.time()

        mem_item = MemoryUnit(timestamp, self.__get_memory())
        self.__memory_list.append(mem_item)

    def __get_memory(self):
        output = self.adb_tools.shell("dumpsys meminfo %s | grep TOTAL" % (self.package_name)).read()
        # print output
        total_memory = 0
        try:
            total_memory = output.strip().split()[1]
        except:
            pass

        return total_memory

class MemoryUnit(object):
    def __init__(self, timestamp, memory):
        self.timestamp = timestamp
        self.memory = memory

    def __str__(self):
        return "%s, memory: %s" %(self.format_time(), str(self.memory))

    def __repr__(self):
        return "{\"timestamp\": %s, \"memory\": %s}" % (self.timestamp, str(self.memory))

    def format_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))


if __name__ == '__main__':
    memory_usage_test = MemoryUsageTest("com.sankuai.meituan", "com.meituan.android.pt.homepage.activity.MainActivity", "005e0f760804", "内存测试")
    # cpu_usage_test.set_up()
    memory_usage_test.start()