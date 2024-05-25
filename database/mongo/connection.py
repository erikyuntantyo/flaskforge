from mongoengine import connect


class Connection:
    """A class represents connection to MongoDB (Example)"""

    def __init__(self, host: str):
        connect(host=host, alias="pysvcdb", uuidRepresentation="standard")
