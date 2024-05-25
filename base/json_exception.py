from flask import jsonify
from utils.constants import CommonExceptions, CommonMessages
from utils.logger import Logger
from werkzeug.wrappers.response import Response


class JSONException(Response):
    """A base class for all JSON exceptions"""

    def __init__(self, response: str | dict = CommonExceptions.INTERNAL_SERVER_ERROR.value, status_code: int = 500, error: str | None = None):
        if not isinstance(response, str):
            try:
                response = jsonify(response)
                mimetype = "application/json"
            except:
                response = str(response)
                mimetype = "text/plain"

        super(JSONException, self).__init__(response, status_code, mimetype="application/json")

        if self.status_code < 400:
            response = jsonify({
                "code": 500,
                "name": CommonExceptions.INTERNAL_SERVER_ERROR.value,
                "message": CommonMessages.HTTP_EXCEPTION_NOT_IMPLEMENTED.value
            })
        else:
            if error is not None:
                Logger.get_instance().error(error)

                response = CommonMessages.INTERNAL_ERROR_ATTENTION.value

            response = jsonify({
                "code": self.status_code,
                "name": self.name,
                "message": response
            })

        self.data = response
        self.headers["Content-Length"] = len(self.data)
        self.mimetype = mimetype

    @property
    def name(self) -> str:
        match(self.status_code):
            case 400: return CommonExceptions.BAD_REQUEST.value
            case 401: return CommonExceptions.UNAUTHORIZED.value
            case 403: return CommonExceptions.FORBIDDEN.value
            case 404: return CommonExceptions.NOT_FOUND.value
            case 405: return CommonExceptions.METHOD_NOT_ALLOWED.value
            case 406: return CommonExceptions.NOT_ACCEPTABLE.value
            case 500: return CommonExceptions.INTERNAL_SERVER_ERROR.value
            case _: return CommonExceptions.UNKNOWN_ERROR.value

    def __str__(self) -> str:
        return f"{self.status_code} {self.name}: {self.response}"


class BadRequest(JSONException):
    """A class represents 400:Bad Request"""

    def __init__(self, response: str | dict = CommonExceptions.BAD_REQUEST.value, error: str | None = None):
        super(BadRequest, self).__init__(response, 400, error)


class Unauthorized(JSONException):
    """A class represents 401:Unauthorized"""

    def __init__(self, response: str | dict = CommonExceptions.UNAUTHORIZED.value, error: str | None = None):
        super(Unauthorized, self).__init__(response, 401, error)


class Forbidden(JSONException):
    """A class represents 403:Forbidden"""

    def __init__(self, response: str | dict = CommonExceptions.FORBIDDEN.value, error: str | None = None):
        super(Forbidden, self).__init__(response, 403, error)


class NotFound(JSONException):
    """A class represents 404:Not Found"""

    def __init__(self, response: str | dict = CommonExceptions.NOT_FOUND.value, error: str | None = None):
        super(NotFound, self).__init__(response, 404, error)


class MethodNotAllowed(JSONException):
    """A class represents 405:Method not Allowed"""

    def __init__(self, response: str | dict = CommonExceptions.METHOD_NOT_ALLOWED.value, error: str | None = None):
        super(MethodNotAllowed, self).__init__(response, 405, error)


class NotAcceptable(JSONException):
    """A class represents 406:Not Acceptable"""

    def __init__(self, response: str | dict = CommonExceptions.NOT_ACCEPTABLE.value, error: str | None = None):
        super(NotAcceptable, self).__init__(response, 406, error)


class InternalServerError(JSONException):
    """A class represents 500:Internal Server Error"""

    def __init__(self, response: str | dict = CommonExceptions.INTERNAL_SERVER_ERROR.value, error: str | None = None):
        super(InternalServerError, self).__init__(response, 500, error)
