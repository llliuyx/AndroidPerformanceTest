#!/usr/bin/evn python
# -*- coding:utf-8 -*-

import yaml
import pyclbr
from performancebasetest.test_suite import PerformanceTestSuite
from performancebasetest.test_case import PerformanceTestCase
from utils.log_handler import get_logger

class CaseExecutor(object):
    def __init__(self, case_file):
        self.case_file_dict = yaml.load(open(case_file))
        self.case_package = self.__get_case_package(self.case_file_dict["case_dir"])
        self.logger = get_logger(__name__, console=True)
        # print self.case_file_dict

    def start(self):
        suite_list = self.case_file_dict["suite"]
        suite_class_instance_list = self.__get_suite_class_instance(suite_list)
        print suite_class_instance_list

        self.__exec_case(suite_class_instance_list)

    def __get_suite_class_instance(self, suite_list):
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
                print case_module_name
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
            suite_class_instance = suite_class_instance()
            suite_class_instance.suite_set_up()

            for case_class_instance in case_class_list:
                case_class_instance = case_class_instance()
                case_class_instance.set_up()
                case_class_instance.test()
                case_class_instance.tear_down()

            suite_class_instance.suite_tear_down()

    def __get_case_package(self, case_dir):
        if case_dir.startswith("./"):
            case_dir = case_dir[2:]
        if not case_dir.endswith("/"):
            case_dir = case_dir + "/"
        case_package = case_dir.replace("/", ".")

        return case_package

if __name__ == '__main__':

    case_executor = CaseExecutor('case_file.yaml')
    case_executor.start()

    # print __name__
    # print pyclbr.readmodule("start_run").keys()
