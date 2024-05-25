from enum import Enum


class Methods(str, Enum):
    """Represents http methods constants"""

    ALL = "ALL"
    POST = "POST"
    GET = "GET"
    FIND = "FIND"
    PATCH = "PATCH"
    DELETE = "DELETE"


class CommonMessages(str, Enum):
    """Represents common message constants"""

    APP_INITIALIZED_INFO = "App initialized"
    CONFIGURATION_STARTED = "App configuration started..."
    DATA_NOT_FOUND = "Data not found"
    DATA_DELETED = "Data deleted"
    HTTP_EXCEPTION_NOT_IMPLEMENTED = "HTTP exception not implemented"
    INTERNAL_ERROR_ATTENTION = "For detail error, please check log file"
    INVALID_FORMAT = "%s format is invalid"
    INVALID_PATH_NAME_OF_ID = "Not allowed to use id as route path name"
    INVALID_TYPE = "%s type is invalid"
    METHOD_NOT_FOUND = "Please define http methods, at least one method defined, or used METHODS.ALL to activate all methods."
    NOT_AUTHENTICATED = "Not authenticated"
    NOT_AUTHORIZED = "Not authorized"
    PAGE_NOT_FOUND = "Page not found"
    REQUIRED_DATA_NOT_FOUND = "%s are required"
    RESPONSE_NOT_IMPLEMENTED = "HTTP response is not implemented"
    SERVICE_NOT_AVAILABLE = "Service not available"
    SERVICE_NOT_INITIALIZED = "Services have not initialized"
    UNINITIALIZED = "Uninitialized %s"


class CommonExceptions(str, Enum):
    """Represents common exception name"""

    BAD_REQUEST = "Bad request"
    FORBIDDEN = "Forbidden"
    INTERNAL_SERVER_ERROR = "Internal server error"
    METHOD_NOT_ALLOWED = "Method not allowed"
    NOT_ACCEPTABLE = "Not acceptable"
    NOT_FOUND = "Not found"
    UNAUTHORIZED = "Unauthorized"
    UNKNOWN_ERROR = "Unknown error"


class CommonResponses(str, Enum):
    """Represents common response name"""

    ACCEPTED = "Accepted"
    CREATED = "Created"
    OK = "OK"
    UNKNOWN_RESPONSE = "Unknown response"
