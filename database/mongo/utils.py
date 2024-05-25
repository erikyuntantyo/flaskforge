import re
from mongoengine import (BooleanField, ComplexDateTimeField, DateTimeField,
                         DecimalField, DictField, Document, EmbeddedDocument,
                         EmbeddedDocumentField, FloatField, IntField,
                         ListField, ObjectIdField, StringField)


class Utils:
    """A utility class represents functions for mongo object"""

    @staticmethod
    def __list_field_to_dict(list_field) -> list:
        rest = []

        for item in list_field:
            if isinstance(item, EmbeddedDocument):
                rest.append(Utils.mongo_to_dict(item, []))
            else:
                rest.append(Utils.__mongo_to_python_type(item, item))

        return rest

    @staticmethod
    def __mongo_to_python_type(field: str, data) -> any:
        if isinstance(field, DateTimeField):
            return str(data.isoformat())
        elif isinstance(field, ComplexDateTimeField):
            return field.to_python(data).isoformat()
        elif isinstance(field, StringField):
            return str(data)
        elif isinstance(field, FloatField):
            return float(data)
        elif isinstance(field, IntField):
            return int(data)
        elif isinstance(field, BooleanField):
            return bool(data)
        elif isinstance(field, ObjectIdField):
            return str(data)
        elif isinstance(field, DecimalField):
            return data
        else:
            return str(data)

    @staticmethod
    def mongo_to_dict(obj: Document, exclude_fields: list[str] = []) -> dict[str, any]:
        rest = []

        if obj is None:
            return None

        if isinstance(obj, Document):
            rest.append(("id", str(obj.id)))

        for field_name in obj._fields:
            if field_name is not None and field_name in exclude_fields:
                continue

            if field_name in ("id",):
                continue

            data = obj._data[field_name]

            if isinstance(obj._fields[field_name], ListField):
                rest.append((field_name, Utils.__list_field_to_dict(data)))
            elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
                rest.append((field_name, Utils.mongo_to_dict(data, [])))
            elif isinstance(obj._fields[field_name], DictField):
                rest.append((field_name, data))
            else:
                rest.append((field_name, Utils.__mongo_to_python_type(obj._fields[field_name], data)))

        return dict(rest)

    @staticmethod
    def query_to_mongo(query: dict[str, any], **default: dict[str, any]) -> dict[str, any]:
        rest: dict = {**{"skip": 0, "limit": 0}, **default, "fields": {}}

        if query is not None:
            for q in query:
                if q == "limit" or q == "skip":
                    rest[q] = query[q]
                    continue
                else:
                    current_query = re.sub(r"(\.)(gt|gte|lt|lte|ne|in|nin|exists|contains|regex)", r"__\2", q)
                    rest["fields"][current_query] = query[q]

        return rest
