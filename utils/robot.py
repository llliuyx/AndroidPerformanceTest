from uiautomator import Device
from utils.Adb import Adb
from time import sleep

class Robot(object):

    def __init__(self, package_name, activity_name, device_serial):
        self.package_name = package_name
        self.activity_name = activity_name
        self.device_serial = device_serial
        self.device = Device(device_serial)

    def start_app(self, pkg_name=None, activity_name=None):
        pkg_name = pkg_name if pkg_name else self.package_name
        activity_name = activity_name if activity_name else self.activity_name
        start_app_cmd = "am start %s/%s" % (pkg_name, activity_name)
        Adb.adb_shell(self.device_serial, start_app_cmd)
        sleep(5)

    def stop_app(self, pkg_name=None):
        pkg_name = pkg_name if pkg_name else self.package_name
        stop_app_cmd = "am force-stop %s" % (pkg_name)
        Adb.adb_shell(self.device_serial, stop_app_cmd)
        sleep(1)

    def clear_app(self, pkg_name=None):
        pkg_name = pkg_name if pkg_name else self.package_name
        clear_app_cmd = "pm clear %s" % (pkg_name)
        Adb.adb_shell(self.device_serial, clear_app_cmd)
        sleep(1)