import MySQLdb

class SqlHandler(object):
    def __init__(self):
        self.connect = MySQLdb.connect("localhost", "root", "qmy123456", "android_performance_test", charset='utf8')

    def create_task(self, phone_model, device_serial, start_time, status):
        insert_sql = "INSERT INTO perf_tasks (device_model, device_serial, start_time, status) VALUES (%s, %s, %s, %s)"
        cursor = self.connect.cursor()
        try:
            cursor.execute(insert_sql, [phone_model, device_serial, start_time, status])
            self.connect.commit()
            task_id = cursor.lastrowid
        except Exception, e:
            print repr(e)
            self.connect.rollback()
            task_id = -1

        return task_id

    def insert_suite(self, task_id, suite_name, app_name, app_version, pkg_name):
        print  task_id, suite_name, app_name, app_version, pkg_name
        insert_sql = "INSERT INTO perf_suites (task_id, suite_name, app_name, app_version, pkg_name) VALUES (%s, %s, %s, %s, %s)"
        cursor = self.connect.cursor()
        try:
            cursor.execute(insert_sql, [task_id, suite_name, app_name, app_version, pkg_name])
            self.connect.commit()
            suite_id = cursor.lastrowid
        except Exception, e:
            print repr(e)
            self.connect.rollback()
            suite_id = -1

        return suite_id

    def insert_cases(self, args):
        insert_sql = "INSERT INTO perf_cases (suite_id, case_name, case_chinese_name, type, status) VALUES (%s, %s, %s, %s, %s)"
        cursor = self.connect.cursor()
        try:
            row_affected_count = cursor.executemany(insert_sql, args)
            self.connect.commit()
        except Exception, e:
            print repr(e)
            self.connect.rollback()
            row_affected_count = 0

        return row_affected_count

    def select_cases_by_task_id(self, task_id):
        select_sql = "SELECT perf_cases.id, case_name, status, suite_name FROM perf_cases INNER JOIN perf_suites ON perf_cases.suite_id = perf_suites.id WHERE task_id = %s AND status != 0"
        cursor = self.connect.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(select_sql, [task_id])
            data = cursor.fetchall()
        except Exception, e:
            print repr(e)
            data = tuple()

        return data

    def update_case_result_by_case_id(self, case_id, status, result):
        if isinstance(result, str):
            result = repr(result)

        update_sql = "UPDATE perf_cases SET status = %s, result = %s WHERE id = %s"
        cursor = self.connect.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        try:
            row_affected_count = cursor.execute(update_sql, [status, result, case_id])
            self.connect.commit()
        except Exception, e:
            print repr(e)
            self.connect.rollback()
            row_affected_count = 0

        return row_affected_count


sql_handler = SqlHandler()
