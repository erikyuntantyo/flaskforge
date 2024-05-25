import re

from base.json_exception import NotFound
from base.service import Service
from factory.services_list import ServicesList
from flask import Blueprint, Flask, jsonify, request
from utils.constants import CommonMessages, Methods
from werkzeug.wrappers.response import Response

from utils.logger import Logger


class ServiceFactory:
    """Represents service factory class"""

    def __init__(self, app: Flask, config: dict[str, any]):
        self.__app__ = app
        self.__config__ = config
        self.__current__ = 0
        self.__stop__ = 0

        self.__app__.register_error_handler(404, lambda _: NotFound(CommonMessages.SERVICE_NOT_AVAILABLE.value))

    def __new__(cls, app, config):
        return super(ServiceFactory, cls).__new__(cls)

    def __iter__(self):
        return self

    def __next__(self) -> int:
        self.__current__ += 1

        if self.__current__ < self.__stop__:
            return self.__current__

        raise StopIteration

    def __register_route__(self, route: str, service: Service):
        if service is None:
            raise ValueError(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "service")
        elif not isinstance(service, Service):
            raise TypeError(CommonMessages.INVALID_TYPE.value % "service")

        route = route.lower()
        prefix = re.match(r"^(\/\w+)+(?<!\/)", route)
        suffix = re.match(r"^.*(\/<(\w+)>)$", route)
        has_prefix = prefix is not None
        has_suffix = suffix is not None

        if has_suffix and "id" in suffix[1]:
            raise ValueError(CommonMessages.INVALID_PATH_NAME_OF_ID.value)

        if not has_prefix or (has_suffix and f"{prefix[0]}{suffix[1]}" != suffix[0]):
            raise ValueError(CommonMessages.INVALID_FORMAT.value % "route")
        else:
            route = f"{prefix[0]}{suffix[1]}" if has_suffix else prefix[0]

        Logger.get_instance().debug(f" * Initialized route {route}")

        service.config = self.__config__
        service.api_version = self.__config__.get("API_VERSION")
        service.service = ServicesList.get_instance().service

        def index_func():
            return jsonify({"apiVersion": service.api_version})

        def common_func(**kwargs) -> Response:
            id: str = kwargs.get("id")
            data: dict = request.get_json(silent=True, force=True)
            file = request.files.get("file")
            headers: dict = dict(request.headers)
            query: dict = dict(request.args)
            params: dict = {"headers": headers, "query": query, "file": file, "id": id}

            if has_suffix:
                params[suffix[2]] = kwargs.get(suffix[2])

            match request.method:
                case Methods.POST:
                    del params["query"]
                    return service.create(data, **params)
                case Methods.DELETE:
                    return service.delete(**params)
                case Methods.PATCH:
                    return service.patch(data, **params)
                case _:
                    if params.get(id) is None:
                        return service.find(**params)
                    else:
                        return service.get(**params)

        blueprint: Blueprint = Blueprint(f"{type(service).__name__.lower()}_blueprint", __name__)

        # create index blueprint
        blueprint.add_url_rule("/", "/", index_func, methods=[Methods.GET.value])

        for method in Methods:
            if (method in service.actions or Methods.ALL in service.actions) and method != Methods.ALL:
                __route__: str = "%s" % (("%s/<id>" % route) if method not in [Methods.POST, Methods.FIND] else route)
                __method__: str = method.value if method != Methods.FIND else Methods.GET.value

                blueprint.add_url_rule(__route__, __route__, common_func, methods=[__method__])

        self.__app__.register_blueprint(blueprint)

    def register_routes(self, services: dict[str, Service]):
        for route, service in services.items():
            self.__register_route__(route, service)
            ServicesList.get_instance().append(route, service)

    @staticmethod
    def create_factory(app: Flask, config: dict[str, any]) -> "ServiceFactory":
        if not hasattr(ServiceFactory, "factory"):
            ServiceFactory.factory = ServiceFactory(app, config)

        return ServiceFactory.factory
