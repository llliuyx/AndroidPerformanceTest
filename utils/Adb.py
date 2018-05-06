#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess
import os

class Adb(object):

    @staticmethod
    def exec_shell_cmd(device_serial, cmd_base):
        if not "ANDROID_HOME" in os.environ.keys():
            print "请设置ANDROID_HOME环境变量"
            exit(-1)

        adb = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
        cmd_line = "%s -s %s shell %s" % (adb, device_serial, cmd_base)
        print cmd_line
        return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    def get_devices():
        """
        获取设备列表
        :return:
        """
        cmd = "adb devices"
        lines = os.popen(cmd).readlines()
        device_list = []
        for i in lines:
            if i.startswith("List of devices attached"):
                continue
            if "device" in i:
                device_list.append(i.split()[0])

        return device_list

    @staticmethod
    def adb_shell(device_serial, cmd):
        """
        执行adb shell命令
        :param args:参数
        :return:
        """
        if not "ANDROID_HOME" in os.environ.keys():
            print "请设置ANDROID_HOME环境变量"
            exit(-1)
        adb = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
        cmd_line = "%s -s %s shell %s" % (adb, device_serial, cmd)
        print cmd_line
        return os.popen(cmd_line)



    # def cmd(self, *args, **kwargs):
    #     '''adb command, add -s serial by default. return the subprocess.Popen object.'''
    #     serial = self.device_serial()
    #     if serial:
    #         if " " in serial:  # TODO how to include special chars on command line
    #             serial = "'%s'" % serial
    #         return self.raw_cmd(*["-s", serial] + list(args))
    #     else:
    #         return self.raw_cmd(*args)
    #
    # def raw_cmd(self, *args):
    #     '''adb command. return the subprocess.Popen object.'''
    #     cmd_line = [self.adb()] + self.adbHostPortOptions + list(args)
    #     if os.name != "nt":
    #         cmd_line = [" ".join(cmd_line)]
    #     return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
