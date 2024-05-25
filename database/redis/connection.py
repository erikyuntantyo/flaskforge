import redis
from utils.constants import CommonMessages


class Connection:
    """A class represents connection to Redis (Example)"""

    def __init__(self, url: str):
        self.cache_manager = redis.Redis.from_url(url)

    def __new__(cls, url: str):
        return super(Connection, cls).__new__(cls)

    @staticmethod
    def connect(url: str):
        if not hasattr(Connection, "cache_manager"):
            Connection.cache_manager = Connection(url).cache_manager

        return Connection.cache_manager

    @staticmethod
    def create(key: str, value: str | dict[str, any], expire: int = 10):
        if Connection.cache_manager is None:
            raise TypeError(CommonMessages.UNINITIALIZED.value % Connection.__name__)

        if isinstance(value, str):
            Connection.cache_manager.set(key, value, expire)
        elif isinstance(value, dict) and all(isinstance(v, str) for v in value.keys()):
            Connection.cache_manager.hset(key, items=value)

    @staticmethod
    def get(key: str, field: str | None = None) -> (str | dict[str, any]):
        if Connection.cache_manager is None:
            raise TypeError(CommonMessages.UNINITIALIZED.value % Connection.__name__)

        if field is None:
            return Connection.cache_manager.get(key)
        else:
            return Connection.cache_manager.hget(key, field)

    @staticmethod
    def delete(key: str, field: str | None = None):
        if Connection.cache_manager is None:
            raise TypeError(CommonMessages.UNINITIALIZED.value % Connection.__name__)

        if field is None:
            return Connection.cache_manager.delete(key)
        else:
            return Connection.cache_manager.hdel(key, field)

    @staticmethod
    def update(key: str, field: str):
        if Connection.cache_manager is None:
            raise TypeError(CommonMessages.UNINITIALIZED.value % Connection.__name__)

        return Connection.cache_manager.hset(key, field)

    @staticmethod
    def publish(key: str):
        if Connection.cache_manager is None:
            raise TypeError(CommonMessages.UNINITIALIZED.value % Connection.__name__)

        # TODO: implement later
        raise NotImplementedError()

    @staticmethod
    def subscribe(key: str):
        if Connection.cache_manager is None:
            raise TypeError(CommonMessages.UNINITIALIZED.value % Connection.__name__)

        # TODO: implement later
        raise NotImplementedError()
