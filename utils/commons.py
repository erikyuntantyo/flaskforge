import functools
import os
import re

import bcrypt
import jwt
from mongoengine import (BooleanField, ComplexDateTimeField, DateTimeField,
                         DecimalField, DictField, Document, EmbeddedDocument,
                         EmbeddedDocumentField, FloatField, IntField,
                         ListField, ObjectIdField, StringField)
from utils.constants import CommonExceptions, CommonMessages


class Auth:
    """Represents authentication common method class"""

    @staticmethod
    def authenticate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                auth = kwargs["headers"]["Authorization"]
                config = args[0].config["AUTH"]

                if auth is not None and config is not None:
                    valid = JWT.validate(auth, config["SECRET"]["PUBLIC_KEY"], [config["JWT"]["HEADERS"]["ALG"]])

                    if valid:
                        func(*args, **kwargs)
                        return

                raise PermissionError(CommonMessages.NOT_AUTHENTICATED.value)
            except:
                raise PermissionError(CommonMessages.NOT_AUTHORIZED.value)

        return wrapper

    @staticmethod
    def check_password(passphrase, hashed_passphrase) -> bool:
        return bcrypt.checkpw(passphrase, hashed_passphrase)

    @staticmethod
    def hash_password(passphrase) -> str:
        return bcrypt.hashpw(passphrase, bcrypt.gensalt(27))


class JWT:
    """Represents JWT common methods class"""

    @staticmethod
    def __is_key_file__(key: str) -> bool:
        try:
            return os.path.isdir(key)
        except:
            return False

    @staticmethod
    def generate(payload: dict[str, any], key: str, headers: dict[str, any] = {"alg": "RS256", "typ": "JWT"}) -> str:
        claims: dict = {"aud": "unknown", "exp": 3600, "iss": "unknown"}
        headers = dict(map(lambda h: (h[0].lower(), h[1]), headers.items()))
        payload = {**claims, **dict(map(lambda p: (p[0].lower(), p[1]), payload.items()))}

        if JWT.__is_key_file__(key):
            with open(key, "r") as f:
                key = f.read()
        else:
            key = key if key is not None else "SECRET_KEY"

        return jwt.encode(payload, key, headers.get("alg"), headers)

    @staticmethod
    def validate(jwt_token: str, key: str, algorithms: list[str] = ["RS256"]) -> bool:
        if JWT.__is_key_file__(key):
            with open(key, "r") as f:
                key = f.read()
        else:
            key = key if key is not None else "SECRET_KEY"

        try:
            return jwt.decode(jwt_token, key, algorithms=algorithms)
        except:
            raise PermissionError(CommonExceptions.UNAUTHORIZED.value)
