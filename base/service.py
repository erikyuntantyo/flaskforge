import traceback

from base.json_exception import (InternalServerError, JSONException,
                                 MethodNotAllowed, NotFound, Unauthorized)
from base.json_response import Created, JsonResponse, Success
from utils.constants import CommonMessages, Methods


class Service:
    """Represents base class for all services"""

    __api_version__: str = "1.0.0"

    def __init__(self, actions: list[Methods] = []) -> None:
        self.actions = actions if actions is not None else []

    @property
    def config(self) -> dict[str, any]:
        return self.__config__

    @config.setter
    def config(self, config: dict):
        self.__config__: dict = config

    @property
    def api_version(self) -> str:
        return self.__api_version__

    @api_version.setter
    def api_version(self, version: str):
        self.__api_version__: str = version

    def on_create(self, data: dict[str, any], **params: dict[str, any]) -> dict[str, any]:
        raise NotImplementedError

    def on_get(self, id: str, **params: dict[str, any]) -> dict[str, any]:
        raise NotImplementedError

    def on_find(self, **params: dict[str, any]) -> dict[str, any]:
        raise NotImplementedError

    def on_patch(self, id: str, data: dict[str, any], **params: dict[str, any]):
        raise NotImplementedError

    def on_delete(self, id: str, **params: dict[str, any]) -> dict[str, any]:
        raise NotImplementedError

    def create(self, data: dict[str, any], **params: dict[str, any]) -> JsonResponse | JSONException:
        try:
            rest = self.on_create(data, **params)

            return Created(rest) if not isinstance(rest, JsonResponse) else rest
        except PermissionError as e:
            return Unauthorized(e)
        except:
            return InternalServerError(CommonMessages.INTERNAL_ERROR_ATTENTION.value, traceback.format_exc())

    def get(self, **params: dict[str, any]) -> JsonResponse | JSONException:
        if params.get("id") is None:
            return MethodNotAllowed(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "<id>")

        try:
            rest = self.on_get(params["id"], **params)

            if rest is None:
                return NotFound(CommonMessages.DATA_NOT_FOUND.value)
            else:
                return Success(rest) if not isinstance(rest, JsonResponse) else rest
        except PermissionError as e:
            return Unauthorized(e)
        except Exception as e:
            return InternalServerError(CommonMessages.INTERNAL_ERROR_ATTENTION. value, traceback.format_exc())

    def find(self, **params: dict[str, any]) -> JsonResponse | JSONException:
        try:
            rest = self.on_find(**params)

            return Success(rest) if not isinstance(rest, JsonResponse) else rest
        except PermissionError as e:
            return Unauthorized(e)
        except:
            return InternalServerError(CommonMessages.INTERNAL_ERROR_ATTENTION. value, traceback.format_exc())

    def patch(self, data: dict[str, any], **params: dict[str, any]) -> JsonResponse | JSONException:
        if params.get("id") is None:
            return MethodNotAllowed(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "<id>")

        if data is None or not data:
            return MethodNotAllowed(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "payload data")

        try:
            rest = self.on_patch(params["id"], data, **params)

            if rest is None:
                return NotFound(CommonMessages.DATA_NOT_FOUND.value)
            else:
                return Success(rest) if not isinstance(rest, JsonResponse) else rest
        except PermissionError as e:
            return Unauthorized(e)
        except:
            return InternalServerError(CommonMessages.INTERNAL_ERROR_ATTENTION. value, traceback.format_exc())

    def delete(self, **params: dict[str, any]) -> JsonResponse | JSONException:
        if params.get("id") is None:
            return MethodNotAllowed(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "<id>")

        try:
            rest = self.on_delete(params["id"], **params)

            return Success(rest) if not isinstance(rest, JsonResponse) else rest
        except PermissionError as e:
            return Unauthorized(e)
        except:
            return InternalServerError(CommonMessages.INTERNAL_ERROR_ATTENTION. value, traceback.format_exc())
