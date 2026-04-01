from uuid import UUID

from paycore_domain.value_objects import EntityId


class TestEntityId:
    def test_generate_creates_valid_uuid(self):
        entity_id = EntityId.generate()
        assert isinstance(entity_id.value, UUID)

    def test_generate_creates_unique_ids(self):
        id1 = EntityId.generate()
        id2 = EntityId.generate()
        assert id1 != id2

    def test_from_string(self):
        raw = "12345678-1234-5678-1234-567812345678"
        entity_id = EntityId.from_string(raw)
        assert entity_id.value == UUID(raw)

    def test_str_returns_uuid_string(self):
        raw = "12345678-1234-5678-1234-567812345678"
        entity_id = EntityId.from_string(raw)
        assert str(entity_id) == raw

    def test_equal_ids_are_equal(self):
        raw = "12345678-1234-5678-1234-567812345678"
        id1 = EntityId.from_string(raw)
        id2 = EntityId.from_string(raw)
        assert id1 == id2

    def test_different_ids_are_not_equal(self):
        id1 = EntityId.generate()
        id2 = EntityId.generate()
        assert id1 != id2
