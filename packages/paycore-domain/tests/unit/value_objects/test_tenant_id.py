from uuid import UUID

from paycore_domain.value_objects import TenantId
from paycore_domain.value_objects.entity_id import EntityId


class TestTenantId:
    def test_generate_creates_valid_uuid(self):
        tenant_id = TenantId.generate()
        assert isinstance(tenant_id.value, UUID)

    def test_generate_returns_tenant_id_type(self):
        tenant_id = TenantId.generate()
        assert isinstance(tenant_id, TenantId)

    def test_from_string(self):
        raw = "12345678-1234-5678-1234-567812345678"
        tenant_id = TenantId.from_string(raw)
        assert tenant_id.value == UUID(raw)

    def test_is_subclass_of_entity_id(self):
        tenant_id = TenantId.generate()
        assert isinstance(tenant_id, EntityId)

    def test_equal_tenant_ids_are_equal(self):
        raw = "12345678-1234-5678-1234-567812345678"
        id1 = TenantId.from_string(raw)
        id2 = TenantId.from_string(raw)
        assert id1 == id2

    def test_different_tenant_ids_are_not_equal(self):
        id1 = TenantId.generate()
        id2 = TenantId.generate()
        assert id1 != id2
