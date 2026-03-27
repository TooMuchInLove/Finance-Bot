from enum import Enum
from typing import Any

from pydantic import ConfigDict, BaseModel as PydanticBaseModel
from pydantic.alias_generators import to_camel


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        kwargs["by_alias"] = True
        kwargs["exclude_none"] = True

        return super().model_dump(*args, **kwargs)


class BaseModelDB(PydanticBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=None
    )

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        kwargs["by_alias"] = True
        kwargs["exclude_none"] = True

        return super().model_dump(*args, **kwargs)


class OrderBy(Enum):
    ASC = "ASC"
    DESC = "DESC"
