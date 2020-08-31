import logging
from logging.handlers import RotatingFileHandler
import os


def init_logger(log_file_name, name="main", limit_log_file_size=True):

    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_file_location = os.path.join(os.getcwd(), "logs", log_file_name)

    # logger
    log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    if limit_log_file_size:
        my_handler = RotatingFileHandler(
            log_file_location,
            mode="a",
            maxBytes=5 * 1024 * 1024,
            backupCount=1,
            encoding=None,
            delay=0,
        )
    else:
        my_handler = logging.FileHandler(log_file_location)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)
    app_log = logging.getLogger(name)
    app_log.setLevel(logging.INFO)
    app_log.addHandler(my_handler)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(log_formatter)
    app_log.addHandler(ch)

    return app_log
