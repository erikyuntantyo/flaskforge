from flask import jsonify
from utils.constants import CommonExceptions, CommonMessages, CommonResponses
from werkzeug.wrappers.response import Response


class JsonResponse(Response):
    """A base class for all json responses"""

    def __init__(self, response: str | dict | list = CommonResponses.OK.value, status_code: int = 200):
        if not isinstance(response, str):
            try:
                response = jsonify(response)
                mimetype = "application/json"
            except:
                response = str(response)
                mimetype = "text/plain"

        super(JsonResponse, self).__init__(response, status_code, mimetype="application/json")

        if status_code > 202:
            response = jsonify({
                "code": 500,
                "name": CommonExceptions.INTERNAL_SERVER_ERROR.value,
                "message": CommonMessages.HTTP_EXCEPTION_NOT_IMPLEMENTED.value
            })

        self.data = response
        self.headers["Content-Length"] = len(self.data)
        self.mimetype = mimetype

    @property
    def name(self) -> str:
        match(self.status_code):
            case 200: return CommonResponses.OK.value
            case 201: return CommonResponses.CREATED.value
            case 202: return CommonResponses.ACCEPTED.value
            case _: return CommonResponses.UNKNOWN_RESPONSE.value

    def __str__(self) -> str:
        return f"{self.status_code} {self.name}: {self.response}"


class Success(JsonResponse):
    """A class represents 200:OK"""

    def __init__(self, response: str | dict | list = CommonResponses.OK.value):
        super(Success, self).__init__(response, 200)


class Created(JsonResponse):
    """A class represents 201:Created"""

    def __init__(self, response: str | dict | list = CommonResponses.CREATED.value):
        super(Created, self).__init__(response, 201)


class Accepted(JsonResponse):
    """A class represents 202:Accepted"""

    def __init__(self, response: str | dict | list = CommonResponses.ACCEPTED.value):
        super(Accepted, self).__init__(response, 202)
