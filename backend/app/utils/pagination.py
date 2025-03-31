from typing import Optional, Tuple
from sqlalchemy.orm import Query


def apply_pagination(
    query: Query,
    limit: int = 20,
    offset: int = 0,
) -> Query:
    return query.offset(offset).limit(limit)


def apply_sorting(
    query: Query,
    model,
    sort_by: Optional[str] = None,
    sort_order: str = "asc"
) -> Query:
    if sort_by:
        column = getattr(model, sort_by, None)
        if column is not None:
            if sort_order.lower() == "desc":
                return query.order_by(column.desc())
            return query.order_by(column.asc())
    return query


def paginate_query(
    query: Query,
    model,
    limit: int = 20,
    offset: int = 0,
    sort_by: Optional[str] = None,
    sort_order: str = "asc"
) -> Tuple[int, list]:
    total = query.count()
    query = apply_sorting(query, model, sort_by, sort_order)
    query = apply_pagination(query, limit, offset)
    return total, query.all()
