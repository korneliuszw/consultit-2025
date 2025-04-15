from typing import Generic, List, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel
from sqlalchemy.orm import Query

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = 1
    size: int = 100


class PaginationResponseSchema(GenericModel, Generic[T]):
    total: int
    page: int
    size: int
    results: List[T]


def paginate(
    query: Query[T], params: PaginationParams, schema: BaseModel = None
) -> PaginationResponseSchema[T]:
    if (params.page < 1) or (params.size < 1):
        raise ValueError(
            "Pagination parameters must be greater than 0. "
            f"page={params.page}, size={params.size}"
        )
    response = query.offset((params.page - 1) * params.size).limit(params.size).all()
    return PaginationResponseSchema(
        total=query.count(),
        page=params.page,
        size=len(response),
        results=(
            response
            if schema == None
            else [schema.model_validate(item) for item in response]
        ),
    )
