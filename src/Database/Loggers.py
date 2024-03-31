import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

from src.shared.Logger import CustomLogger

pre_path = os.getcwd()
postfix = 'database'
print(pre_path)
CameraLogger = CustomLogger("CameraLogs", prefix=pre_path, postfix=postfix)
DetectedBoxLogger = CustomLogger("DetectedBoxLogs", prefix=pre_path, postfix=postfix)
FrameLogger = CustomLogger("FrameLogs", prefix=pre_path, postfix=postfix)
UserLogger = CustomLogger("UserLogs", prefix=pre_path, postfix=postfix)


# Example usage
if __name__ == "__main__":
    custom_logger = CustomLogger("example", prefix=os.getcwd())


    def some_function():
        custom_logger.log("info", "This message is from some function")


    some_function()
