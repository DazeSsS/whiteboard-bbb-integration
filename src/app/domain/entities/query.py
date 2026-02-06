from urllib.parse import urlencode

from pydantic import ConfigDict

from .base import CamelSchema


class QuerySchema(CamelSchema):
    model_config = ConfigDict(
        **CamelSchema.model_config,
        extra='allow',
    )

    def to_query_string(
        self,
        include_fields: list[str] | None = None,
        exclude_fields: list[str] | None = None,
    ):
        data = self.model_dump(
            include=include_fields,
            exclude=exclude_fields,
            by_alias=True,
        )
        query = urlencode(data)
        return query
