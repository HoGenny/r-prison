from dataclasses import dataclass
from typing import Annotated

from fastapi import Query


@dataclass(slots=True)
class CursorPagination:
    cursor: int | None
    limit: int


async def get_pagination(
    cursor: Annotated[int | None, Query(default=None, ge=1)] = None,
    limit: Annotated[int, Query(default=20, ge=1, le=100)] = 20,
) -> CursorPagination:
    return CursorPagination(cursor=cursor, limit=limit)
