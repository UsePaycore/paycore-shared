from uuid import UUID

from paycore_domain.value_objects import UserId
from paycore_domain.value_objects.entity_id import EntityId


class TestUserId:
    def test_generate_creates_valid_uuid(self):
        user_id = UserId.generate()
        assert isinstance(user_id.value, UUID)

    def test_generate_returns_user_id_type(self):
        user_id = UserId.generate()
        assert isinstance(user_id, UserId)

    def test_from_string(self):
        raw = "12345678-1234-5678-1234-567812345678"
        user_id = UserId.from_string(raw)
        assert user_id.value == UUID(raw)

    def test_is_subclass_of_entity_id(self):
        user_id = UserId.generate()
        assert isinstance(user_id, EntityId)

    def test_equal_user_ids_are_equal(self):
        raw = "12345678-1234-5678-1234-567812345678"
        id1 = UserId.from_string(raw)
        id2 = UserId.from_string(raw)
        assert id1 == id2

    def test_different_user_ids_are_not_equal(self):
        id1 = UserId.generate()
        id2 = UserId.generate()
        assert id1 != id2
