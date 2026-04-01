from dataclasses import dataclass

from paycore_domain.cqrs import Query


@dataclass(frozen=True)
class FindUserQuery(Query):
    user_id: str


class TestQuery:
    def test_is_frozen_dataclass(self):
        query = FindUserQuery(user_id="abc-123")
        try:
            query.user_id = "xyz"
            assert False, "Should not reach here"
        except AttributeError:
            pass

    def test_stores_fields(self):
        query = FindUserQuery(user_id="abc-123")
        assert query.user_id == "abc-123"

    def test_equal_queries_are_equal(self):
        q1 = FindUserQuery(user_id="abc-123")
        q2 = FindUserQuery(user_id="abc-123")
        assert q1 == q2

    def test_different_queries_are_not_equal(self):
        q1 = FindUserQuery(user_id="abc-123")
        q2 = FindUserQuery(user_id="xyz-789")
        assert q1 != q2
