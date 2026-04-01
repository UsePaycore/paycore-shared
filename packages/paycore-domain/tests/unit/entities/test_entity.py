from datetime import UTC, datetime

from paycore_domain.entities import Entity
from paycore_domain.value_objects import EntityId


class ConcreteEntity(Entity[EntityId]):
    def __init__(self, id: EntityId, name: str) -> None:
        super().__init__(id)
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class TestEntity:
    def test_stores_id(self):
        entity_id = EntityId.generate()
        entity = ConcreteEntity(id=entity_id, name="Test")
        assert entity.id == entity_id

    def test_sets_created_at_on_init(self):
        before = datetime.now(UTC)
        entity = ConcreteEntity(id=EntityId.generate(), name="Test")
        after = datetime.now(UTC)
        assert before <= entity.created_at <= after

    def test_sets_updated_at_on_init(self):
        before = datetime.now(UTC)
        entity = ConcreteEntity(id=EntityId.generate(), name="Test")
        after = datetime.now(UTC)
        assert before <= entity.updated_at <= after

    def test_update_timestamp_changes_updated_at(self):
        entity = ConcreteEntity(id=EntityId.generate(), name="Test")
        original_updated_at = entity.updated_at
        entity._update_timestamp()
        assert entity.updated_at >= original_updated_at

    def test_entities_with_same_id_are_equal(self):
        entity_id = EntityId.generate()
        entity1 = ConcreteEntity(id=entity_id, name="Alice")
        entity2 = ConcreteEntity(id=entity_id, name="Bob")
        assert entity1 == entity2

    def test_entities_with_different_id_are_not_equal(self):
        entity1 = ConcreteEntity(id=EntityId.generate(), name="Alice")
        entity2 = ConcreteEntity(id=EntityId.generate(), name="Alice")
        assert entity1 != entity2

    def test_entity_not_equal_to_non_entity(self):
        entity = ConcreteEntity(id=EntityId.generate(), name="Test")
        assert entity != "not an entity"

    def test_entities_with_same_id_have_same_hash(self):
        entity_id = EntityId.generate()
        entity1 = ConcreteEntity(id=entity_id, name="Alice")
        entity2 = ConcreteEntity(id=entity_id, name="Bob")
        assert hash(entity1) == hash(entity2)
