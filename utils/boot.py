from io import TextIOWrapper
import yaml
from factory.service_factory import ServiceFactory
from flask import Flask
from flask_compress import Compress
from flask_cors import CORS
from mergedeep import merge

from database.mongo.connection import Connection as MongoConn
from database.redis.connection import Connection as RedisConn
from services.auth import Authentication as AuthSvc
from services.users import Users as UsersSvc
from utils.constants import CommonMessages, Methods
from utils.logger import Logger


class Boot:
    """Represents boot loader class"""

    @staticmethod
    def configure_app(env, app_name) -> Flask:
        if not hasattr(Boot, "app"):
            app: Flask = Flask(__name__)

            CORS(app)
            Compress(app)

            try:
                defaultFile: TextIOWrapper = open("config/default.yaml", "r")
                productionFile: TextIOWrapper = open("config/production.yaml", "r")

                default: dict = yaml.safe_load(defaultFile)
                production: dict = yaml.safe_load(productionFile)
            finally:
                defaultFile.close()
                productionFile.close()

            config: dict = default if env == "development" else merge(default, production)

            Logger.get_instance(app_name, config.get("LOG_LEVEL"), config.get("LOG_PATH")).debug(CommonMessages.CONFIGURATION_STARTED.value)

            app.config.from_mapping(config)

            app.config["ENV"] = env
            app.config["DEBUG"] = env == "development"

            # How to connect database (example)
            MongoConn(config.get("DATABASE"))
            RedisConn.connect(config.get("REDIS"))
            # end database connection

            service_factory: ServiceFactory = ServiceFactory.create_factory(app, config)

            service_factory.register_routes({
                "/auth/<endpoint>": AuthSvc(Methods.POST),  # Allow POST method to be available for the service with custom endpoint
                "/users": UsersSvc()  # Restricted service to be accessed by internal service only
            })

            Boot.app = app
        else:
            app = Boot.app

        return app
