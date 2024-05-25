from base.service import Service
from utils.constants import CommonMessages


class ServicesList:
    """A class represents services list"""

    def __init__(self):
        self.services = {}

    def __new__(cls):
        return super(ServicesList, cls).__new__(cls)

    def append(self, key: str, service: Service):
        if key is None:
            raise ValueError(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "key")

        if service is None:
            raise ValueError(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "service")

        self.services[key.lower() if key[0] != "/" else key[1:].lower()] = service

    def service(self, key: str) -> "ServicesList":
        if not self.services:
            raise TypeError(CommonMessages.SERVICE_NOT_INITIALIZED.value)

        if key is None:
            raise ValueError(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "key")

        self.key = key.lower() if key[0] != "/" else key[1:].lower()

        if key not in self.services:
            raise ValueError(CommonMessages.SERVICE_NOT_AVAILABLE.value)

        return self

    def create(self, data: dict[str, any], **params: dict[str, any]) -> dict[str, any]:
        if self.key is None:
            raise ValueError(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "key")

        return self.services[self.key].create(data, **params)

    def get(self, id: str, **params: dict[str, any]) -> dict[str, any]:
        if self.key is None:
            raise ValueError(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "key")

        return self.services[self.key].get(id, **params)

    def find(self, **params: dict[str, any]) -> dict[str, any]:
        if self.key is None:
            raise ValueError(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "key")

        return self.services[self.key].find(**params)

    def patch(self, id: str, data: dict[str, any], **params: dict[str, any]) -> dict[str, any]:
        if self.key is None:
            raise ValueError(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "key")

        return self.services[self.key].patch(id, data, **params)

    def delete(self, id: str, **params: dict[str, any]) -> dict[str, any]:
        if self.key is None:
            raise ValueError(CommonMessages.REQUIRED_DATA_NOT_FOUND.value % "key")

        return self.services[self.key].delete(id, **params)

    @staticmethod
    def get_instance() -> "ServicesList":
        if not hasattr(ServicesList, "obj"):
            ServicesList.obj = ServicesList()

        return ServicesList.obj
