from base.json_exception import MethodNotAllowed
from base.json_response import Created
from base.service import Service
from utils.constants import CommonMessages


class Authentication(Service):
    """A class represents authentication service"""

    def on_create(self, data: dict[str, any], **params: dict[str, any]) -> dict[str, any]:
        match params.get("custom_endpoint"):
            case "token":
                # TODO: create new token authentication using user_id and password with refresh_token
                # return []
                response = Created([])
                response.set_cookie("refresh-token", "token_data", path="/")

                return response
            case "session":
                # TODO: create session_id
                return []
            case "refresh":
                # TODO: update token
                return []
            case "revoke":
                # TODO: revoke token
                return []
            case _:
                return MethodNotAllowed(CommonMessages.REQUIRED_DATA_NOT_FOUND.value & "<method>")
