import logging
import os
from logging.handlers import TimedRotatingFileHandler


class CustomLogger:
    def __init__(self, name, prefix, postfix, log_level=logging.DEBUG, max_logs=7):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Ensure the logs directory exists
        log_directory = f"{prefix}/logs/{postfix}"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # Setup filename pattern for the log files
        filename = f"{log_directory}/{name}.log"

        # Create a timed rotating file handler
        self.handler = TimedRotatingFileHandler(filename, when="midnight", interval=1, backupCount=max_logs,
                                                encoding="utf-8")

        # Define log format
        log_format = logging.Formatter('%(levelname)s | %(asctime)s | %(funcName)s | %(message)s',
                                       datefmt='%Y_%m_%d__%H_%M_%S')
        self.handler.setFormatter(log_format)

        self.logger.addHandler(self.handler)

    def log(self, level, message, *args, **kwargs):
        """
        Generic log method that logs messages with the specified level.
        """
        if hasattr(self.logger, level):
            log_method = getattr(self.logger, level)
            log_method(message, *args, **kwargs)
        else:
            self.logger.error(f"Log level '{level}' is not valid.")
