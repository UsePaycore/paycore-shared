from dataclasses import dataclass
from uuid import UUID

from paycore_domain.value_objects.primitives import UuidValueObject


@dataclass(frozen=True)
class OrderId(UuidValueObject):
    pass


class TestUuidValueObject:
    def test_stores_uuid_value(self):
        uid = UUID("12345678-1234-5678-1234-567812345678")
        order_id = OrderId(value=uid)
        assert order_id.value == uid

    def test_coerces_string_to_uuid(self):
        order_id = OrderId(value="12345678-1234-5678-1234-567812345678")
        assert isinstance(order_id.value, UUID)
        assert order_id.value == UUID("12345678-1234-5678-1234-567812345678")

    def test_generate_creates_new_uuid(self):
        order_id = OrderId.generate()
        assert isinstance(order_id.value, UUID)

    def test_generate_creates_unique_ids(self):
        id1 = OrderId.generate()
        id2 = OrderId.generate()
        assert id1 != id2

    def test_from_string(self):
        order_id = OrderId.from_string("12345678-1234-5678-1234-567812345678")
        assert order_id.value == UUID("12345678-1234-5678-1234-567812345678")

    def test_str_returns_string_representation(self):
        uid = UUID("12345678-1234-5678-1234-567812345678")
        order_id = OrderId(value=uid)
        assert str(order_id) == "12345678-1234-5678-1234-567812345678"

    def test_repr_includes_class_name(self):
        uid = UUID("12345678-1234-5678-1234-567812345678")
        order_id = OrderId(value=uid)
        assert "OrderId" in repr(order_id)

    def test_equal_objects_are_equal(self):
        uid = UUID("12345678-1234-5678-1234-567812345678")
        assert OrderId(value=uid) == OrderId(value=uid)

    def test_different_objects_are_not_equal(self):
        id1 = OrderId.generate()
        id2 = OrderId.generate()
        assert id1 != id2
