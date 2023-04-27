from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class IDMixin(BaseModel):
    _id: str


class CreateAtMixin(BaseModel):
    create_at: str = datetime.now()


class Status(BaseModel):
    status: Union[str, bool]


class SortBy(BaseModel):
    sort_field: Optional[str]
