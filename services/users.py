from base.service import Service
from database.mongo.models.users import Users as UsersCollection
from database.mongo.utils import Utils
# from utils.commons import Auth


class Users(Service):
    """A class represents users service (Example)"""

    # @Auth.authenticate
    def on_get(self, id: str, **params: dict[str, any]) -> dict[str, any]:
        query: dict = Utils.query_to_mongo(params.get("query"))
        usersCollection = UsersCollection(id=id, **query.get("fields"))

        return Utils.mongo_to_dict(usersCollection)
