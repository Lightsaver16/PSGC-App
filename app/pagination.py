from typing import TypeVar

from fastapi_pagination.links import Page
from fastapi_pagination.customization import CustomizedPage, UseParamsFields

T = TypeVar("T")

DefaultPage = CustomizedPage[
    Page[T],
    UseParamsFields(size=10)
]
