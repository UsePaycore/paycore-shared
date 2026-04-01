from dataclasses import dataclass
from typing import Optional

from paycore_domain.cqrs import Query, QueryHandler


@dataclass(frozen=True)
class GetUserQuery(Query):
    user_id: str


class GetUserQueryHandler(QueryHandler[GetUserQuery, Optional[dict]]):
    def __init__(self) -> None:
        self._users = {
            "1": {"id": "1", "name": "Alice"},
            "2": {"id": "2", "name": "Bob"},
        }

    def handle(self, query: GetUserQuery) -> Optional[dict]:
        return self._users.get(query.user_id)


class TestQueryHandler:
    def test_handle_returns_found_result(self):
        handler = GetUserQueryHandler()
        result = handler.handle(GetUserQuery(user_id="1"))
        assert result == {"id": "1", "name": "Alice"}

    def test_handle_returns_none_for_missing(self):
        handler = GetUserQueryHandler()
        result = handler.handle(GetUserQuery(user_id="999"))
        assert result is None
