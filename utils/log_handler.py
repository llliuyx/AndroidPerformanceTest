import logging
import time

def get_logger(name, level=logging.DEBUG, console=False):
    # log_file = "android-performance-test-log-%s.txt" % time.strftime("%Y%m%d%H%M%S", time.localtime())
    #
    # logger = logging.getLogger(name)
    # logger.setLevel(level=level)
    # handler = logging.FileHandler(log_file)
    # handler.setLevel(level=level)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    #
    # logger.addHandler(handler)
    #
    # if console:
    #     console = logging.StreamHandler()
    #     console.setLevel(level)
    #     logger.addHandler(console)

    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(name)

    return logger

if __name__ == '__main__':
    get_logger(__name__)