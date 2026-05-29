from typing import Generic
from typing import TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error: str | None = None
