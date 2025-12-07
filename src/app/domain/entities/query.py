from urllib.parse import urlencode
from pydantic import ConfigDict

from .base import CamelSchema


class QuerySchema(CamelSchema):
    model_config = ConfigDict(
        **CamelSchema.model_config,
        extra='allow',
    )
    
    def to_query_string(self):
        data = self.model_dump(by_alias=True)
        query = urlencode(data)
        return query
