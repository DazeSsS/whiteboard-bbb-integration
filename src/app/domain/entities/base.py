from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


class CamelSchema(BaseSchema):
    model_config = ConfigDict(
        **BaseSchema.model_config,
        alias_generator=to_camel,
    )
