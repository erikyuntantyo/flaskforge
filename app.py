import pray
from flask import Flask
from utils.boot import Boot
from utils.constants import CommonMessages
from utils.logger import Logger


class App:
    """A class represents app initialization"""

    def __init__(self, env="development"):
        self.app = Boot.configure_app(env, "forged-service")
        Logger.get_instance().debug(CommonMessages.APP_INITIALIZED_INFO.value)

    def run(self):
        return self.app.run()


if __name__ == "__main__":
    App("development").run()
else:
    gunicorn = App('production').app
