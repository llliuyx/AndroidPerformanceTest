CREATE DATABASE android_performance_test;

CREATE TABLE perf_tasks
(
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  device_model VARCHAR(25),
  device_serial VARCHAR(25),
  start_time VARCHAR(20),
  end_time VARCHAR(20),
  status INTEGER
) DEFAULT CHARSET=utf8;

CREATE TABLE perf_suites
(
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  task_id INTEGER,
  suite_name VARCHAR(255),
  app_name VARCHAR(20),
  app_version VARCHAR(10),
  pkg_name VARCHAR(50),
  FOREIGN KEY(task_id) REFERENCES perf_tasks(id) ON UPDATE CASCADE ON DELETE CASCADE
) DEFAULT CHARSET=utf8;

CREATE TABLE perf_cases
(
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  suite_id INTEGER,
  case_name VARCHAR(255),
  case_chinese_name VARCHAR(50),
  type VARCHAR(10),
  status INTEGER,
  result TEXT,
  FOREIGN KEY(suite_id) REFERENCES perf_suites(id) ON UPDATE CASCADE ON DELETE CASCADE
) DEFAULT CHARSET=utf8;