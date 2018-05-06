#!/usr/bin/evn python
# -*- coding:utf-8 -*-

import yaml
import pyclbr
import time
from performancebasetest.test_suite import PerformanceTestSuite
from performancebasetest.test_case import PerformanceTestCase
from utils.log_handler import get_logger
from utils.Adb import Adb
from utils.sql_handler import sql_handler
from enum import Enum

class CaseExecutor(object):
    RUN_TYPE_ENUM = Enum("RUN_TIPE_ENUM", ("release", "debug"))
    def __init__(self, case_file):
        self.case_file_dict = yaml.load(open(case_file))
        self.case_package = self.__get_case_package(self.case_file_dict["case_dir"])
        self.logger = get_logger(__name__, console=True)
        self.run_type = self.__get_run_type(self.case_file_dict["run_type"])
        self.task_id = self.case_file_dict["task_id"]
        self.device_serial = self.__get_device_serial(self.case_file_dict["device_serial"])

    def start(self):
        suite_list = self.case_file_dict["suite"]
        suite_case_class_list = self.__suite_case_str_to_class(suite_list)

        case_list = list()
        if self.run_type == self.__class__.RUN_TYPE_ENUM.release:
            self.logger.info("run_type: release")
            if self.task_id == -1:
                self.__create_task_db(suite_case_class_list)
            case_list = self.__get_case_from_task_db()
        elif self.run_type == self.__class__.RUN_TYPE_ENUM.debug:
            self.logger.info("run_type: debug")
            case_list = self.__get_case_from_yaml(suite_case_class_list)

        self.logger.info("case_list: " + repr(case_list))
        self.__exec_case(case_list)

    def __get_case_from_yaml(self, suite_list):
        i = 0
        for suite_item in suite_list:
            case_class_list = suite_item["case"]
            case_class_list_temp = list()
            for case_class_item in case_class_list:
                case_class_dict = {"case_class": case_class_item, "case_id": -1L}
                case_class_list_temp.append(case_class_dict)

            suite_list[i]["case"] = case_class_list_temp
            i += 1

        return suite_list


    def __get_case_from_task_db(self):
        def class_str_to_class(class_str):
            module_name = class_str[:class_str.rfind(".")]
            class_name = class_str[class_str.rfind(".") + 1:]
            class_module = __import__(module_name, fromlist=[class_name])
            return class_module.__dict__[class_name]

        self.logger.info("获取测试任务：task_id: %s", self.task_id)
        suite_case_tuple = sql_handler.select_cases_by_task_id(self.task_id)
        ret_case_list = list()
        suite_list_helper = list()
        for suite_case_item in suite_case_tuple:
            suite_name = suite_case_item["suite_name"]
            case_name = suite_case_item["case_name"]
            case_id = suite_case_item["id"]
            suite_class = class_str_to_class(suite_name)
            case_class = class_str_to_class(case_name)
            if not suite_name in suite_list_helper:
                ret_dict = {"suite": suite_class, "case": [{"case_class": case_class, "case_id": case_id}]}
                ret_case_list.append(ret_dict)
                suite_list_helper.append(suite_name)
            else:
                index = len(suite_list_helper)
                ret_case_list[index - 1]["case"].append({"case_class": case_class, "case_id": case_id})

        return ret_case_list

    def __create_task_db(self, suite_list):
        def create_task():
            phone_model = Adb.adb_shell(self.device_serial, "'getprop ro.product.model'").readlines()[0].strip()
            start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            task_id = sql_handler.create_task(phone_model, self.device_serial, start_time_str, 1)
            return task_id

        def insert_suite():
            cmd = "dumpsys package %s | grep  versionName" % pkg_name
            version_name_output =Adb.adb_shell(self.device_serial, cmd).readlines()
            if len(version_name_output) == 0 or len(version_name_output[0].split("=")) != 2:
                self.logger.error("未安装%s(%s)应用" % (app_name, pkg_name))
                version_name_output = ["versionName="]
            version_name_list = version_name_output[0].split("=")
            version_name = version_name_list[1].strip()
            suite_id = sql_handler.insert_suite(self.task_id, suite_name, app_name, version_name, pkg_name)
            return suite_id

        self.task_id = create_task()
        self.logger.info("创建task，task_id: %s", self.task_id)
        if self.task_id == -1:
            self.logger.error("创建任务失败")
            exit(-1)
        for suite_case_item in suite_list:
            suite_class = suite_case_item["suite"]
            suite_object_instance = suite_class(self.device_serial)
            suite_name = "%s.%s" % (suite_class.__module__, suite_class.__name__)
            app_name = suite_object_instance.app_name.strip()
            pkg_name = suite_object_instance.package_name.strip()
            suite_id = insert_suite()
            if suite_id == -1:
                self.logger.error("插入 %s Suite 失败" % suite_name)

            case_list = list()
            for case_item in suite_case_item["case"]:
                print case_item
                case_object_instance = case_item(self.device_serial)
                suite_id = suite_id
                case_name = "%s.%s" % (case_item.__module__, case_item.__name__)
                case_chinese_name = case_object_instance.case_chinese_name
                case_type = case_object_instance.type
                status = 1
                case_list.append([suite_id, case_name, case_chinese_name, case_type, status])
            sql_handler.insert_cases(case_list)

    def __suite_case_str_to_class(self, suite_list):
        suite_class_instance_list = []
        for suite_item in suite_list:
            suite_module_name = self.case_package + suite_item["name"]
            suite_class_list = pyclbr.readmodule(suite_module_name).keys()
            if len(suite_class_list) != 1:
                self.logger.error("%s模块中测试类个数不为1，该Suite类将会被跳过.", suite_module_name)
                continue

            suite_module = __import__(suite_module_name, fromlist=suite_class_list)
            suite_class_instance = suite_module.__dict__[suite_class_list[0]]
            if not issubclass(suite_class_instance, PerformanceTestSuite):
                self.logger.error("%s Suite类不是 %s 子类，该Suite类将会被跳过.", suite_class_instance.__name__,
                                  PerformanceTestSuite.__name__)
                continue

            case_class_instance_list = []
            for case_item in suite_item["case"]:
                case_module_name = self.case_package + case_item
                case_class_list = pyclbr.readmodule(case_module_name).keys()
                if len(case_class_list) != 1:
                    self.logger.error("%s模块中测试类个数不为1，该Case类将会被跳过.", case_module_name)
                    continue
                case_module = __import__(case_module_name, fromlist=case_class_list)
                case_class_instance = case_module.__dict__[case_class_list[0]]
                if not issubclass(case_class_instance, PerformanceTestCase):
                    self.logger.error("%s Case类不是 %s 子类，该Case类将会被跳过.", case_class_instance.__name__,
                                      PerformanceTestCase.__name__)
                    continue
                case_class_instance_list.append(case_class_instance)
            suite_class_instance_list.append({"suite": suite_class_instance, "case": case_class_instance_list})

        return suite_class_instance_list

    def __exec_case(self, suite_case_list):
        for suite_case_item in suite_case_list:
            suite_class_instance = suite_case_item["suite"]
            case_class_list = suite_case_item["case"]
            suite_class_instance = suite_class_instance(self.device_serial)
            suite_class_instance.suite_set_up()

            for case_item in case_class_list:
                case_id = case_item["case_id"]
                case_class_instance = case_item["case_class"]
                case_class_instance = case_class_instance(self.device_serial)
                case_class_instance.set_up()
                case_class_instance.start()
                case_class_instance.test()
                case_class_instance.end()
                case_class_instance.tear_down()

                if self.run_type == self.__class__.RUN_TYPE_ENUM.release:
                    case_result = case_class_instance.results
                    sql_handler.update_case_result_by_case_id(case_id, 0, repr(case_result))
                elif self.run_type == self.__class__.RUN_TYPE_ENUM.debug:
                    pass

            suite_class_instance.suite_tear_down()

    def __get_case_package(self, case_dir):
        if case_dir.startswith("./"):
            case_dir = case_dir[2:]
        if not case_dir.endswith("/"):
            case_dir = case_dir + "/"
        case_package = case_dir.replace("/", ".")

        return case_package

    def __get_run_type(self, run_type):
        enum_key_list = self.__class__.RUN_TYPE_ENUM.__members__.keys()
        if not run_type in enum_key_list:
            self.logger.error("run_type 值只能为 " + " or ".join(enum_key_list))
            exit(-1)

        return self.__class__.RUN_TYPE_ENUM[run_type]

    def __get_device_serial(self, device_serial):
        device_connected_list = Adb.get_devices()
        if not device_serial in device_connected_list:
            self.logger.error("PC 未连接该设备 %s" % self.device_serial)
            exit(-1)

        return device_serial


if __name__ == '__main__':

    case_executor = CaseExecutor('case_file.yaml')
    case_executor.start()

    # print __name__
    # print pyclbr.readmodule("start_run").keys()
