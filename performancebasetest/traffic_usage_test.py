#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from performancebasetest.test_case import PerformanceTestCase
import threading
import time
from abc import ABCMeta, abstractmethod

class TrafficUsageTest(PerformanceTestCase):
    """
    流量测试基础类
    """
    __metaclass__ = ABCMeta
    def __init__(self, package_name, activity_name, device_serial, case_chinese_name, log=None):
        super(TrafficUsageTest, self).__init__(package_name, activity_name, device_serial, case_chinese_name, log)
        self.is_finished = True
        self.__traffic_list = []
        self.robot.start_app()
        self.pid = self.adb_tools.get_pid(self.package_name)
        self.uid = self.adb_tools.get_uid(self.pid)
        self.robot.stop_app()
        self.is_first = True

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
        return "traffic"

    @property
    def results(self):
        return self.__traffic_list

    def start(self):
        self.timer = threading.Timer(1, self.__fun_get_traffics)
        self.timer.start()

    def end(self):
        self.timer.cancel()
        print self.results

    def __fun_get_traffics(self):
        self.timer = threading.Timer(5, self.__fun_get_traffics)
        self.timer.start()

        current_timestamp = time.time()
        tcp_rcv, tcp_snd = self.__get_traffic()

        if self.is_first:
            self.is_first = False
            self.__start_jiffs_item = TrafficsUnit(current_timestamp, tcp_rcv, tcp_snd)
            self.__last_tcp_rcv = tcp_rcv
            self.__last_tcp_snd = tcp_snd
        elif tcp_rcv > 0 and tcp_snd > 0:
            rcv = tcp_rcv - self.__last_tcp_rcv
            snd = tcp_snd - self.__last_tcp_snd
            traffics_unit = TrafficsUnit(current_timestamp, rcv, snd)
            traffics_string = traffics_unit.__str__()
            print traffics_string
            # self.log.info(jiffs_string)
            self.__traffic_list.append(traffics_unit)
            self.__last_tcp_rcv = tcp_rcv
            self.__last_tcp_snd = tcp_snd

    def __get_traffic(self):
        tcp_rcv = self.adb_tools.shell("cat /proc/uid_stat/%s/tcp_rcv" % self.uid).read().strip()
        tcp_snd = self.adb_tools.shell("cat /proc/uid_stat/%s/tcp_snd" % self.uid).read().strip()

        tcp_rcv = int(tcp_rcv) if tcp_rcv else 0
        tcp_snd = int(tcp_snd) if tcp_snd else 0

        return tcp_rcv, tcp_snd

class TrafficsUnit(object):
    def __init__(self, timestamp, tcp_scv, tcp_snd):
        self.timestamp = timestamp
        self.tcp_scv = tcp_scv
        self.tcp_snd = tcp_snd

    def __str__(self):
        return "%s, tcp_scv: %s, tcp_snd: %s" %(self.format_time(), str(self.tcp_scv), str(self.tcp_snd))

    def __repr__(self):
        return "{\"tcp_scv\": %s, \"tcp_snd\": %s}" % (str(self.tcp_scv), str(self.tcp_snd))

    def format_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))


if __name__ == '__main__':
    traffic_usage_test = TrafficUsageTest("com.sankuai.meituan", "com.meituan.android.pt.homepage.activity.MainActivity", "005e0f760804", "流量测试")
    traffic_usage_test.start()