import logging
import os

from utils.constants import CommonMessages


class Logger:
    """A class to repressent logger"""

    def __init__(self, name: str = "app", level: str = "DEBUG", path: str = "./logs"):
        config = {"name": name, "LOG_LEVEL": level, "LOG_PATH": path}
        name = "%s.app" % config["name"].lower().replace(".log", "")
        logger = logging.getLogger(name)

        logger.setLevel(config["LOG_LEVEL"])

        if len(logger.handlers) == 0:
            if not os.path.exists(config["LOG_PATH"]):
                os.mkdir(config["LOG_PATH"])

            filename = os.path.join(config["LOG_PATH"], "%s.log" % name)
            handler = logging.FileHandler(filename)
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)s %(message)s", "%Y-%m-%d %H:%M:%S")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        self.logger = logger

    def __new__(cls, name: str, level: str, path: str):
        return super(Logger, cls).__new__(cls)

    @staticmethod
    def get_instance(name: str | None = None, level: str | None = None, path: str | None = None) -> logging.Logger:
        if not hasattr(Logger, "logger"):
            if name is None or level is None or path is None:
                raise ValueError(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "name, level, path")

            Logger.logger = Logger(name, level, path).logger

        return Logger.logger
