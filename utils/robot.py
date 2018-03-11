from uiautomator import Device
from utils.Adb import Adb
from time import sleep

class Robot(object):

    def __init__(self, package_name, activity_name, device_serial):
        self.package_name = package_name
        self.activity_name = activity_name
        self.device_serial = device_serial
        self.device = Device(device_serial)

    def start_app(self):
        start_app_cmd = "am start %s/%s" % (self.package_name, self.activity_name)
        Adb.exec_shell_cmd(self.device_serial, start_app_cmd)
        sleep(5)

    def stop_app(self):
        stop_app_cmd = "am force-stop %s" % (self.package_name)
        Adb.exec_shell_cmd(self.device_serial, stop_app_cmd)
        sleep(1)

    def clear_app(self):
        clear_app_cmd = "pm clear %s" % (self.package_name)
        Adb.exec_shell_cmd(self.device_serial, clear_app_cmd)
        sleep(1)