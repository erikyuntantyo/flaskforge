from mongoengine import Document, EmailField, StringField


class Users(Document):
    """A class represents users data model (Example)"""

    meta = {"db_alias":"pysvcdb"}

    username = StringField(required=True, unique=True)
    email = EmailField(required=True)
    fullname = StringField(required=True)
