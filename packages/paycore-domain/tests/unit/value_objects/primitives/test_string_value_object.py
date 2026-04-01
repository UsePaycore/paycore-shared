from dataclasses import dataclass

from paycore_domain.value_objects.primitives import StringValueObject


@dataclass(frozen=True)
class Name(StringValueObject):
    pass


class TestStringValueObject:
    def test_stores_value(self):
        name = Name(value="Alice")
        assert name.value == "Alice"

    def test_str_returns_value(self):
        name = Name(value="Alice")
        assert str(name) == "Alice"

    def test_repr_includes_class_name(self):
        name = Name(value="Alice")
        assert "Name" in repr(name)

    def test_equal_objects_are_equal(self):
        name1 = Name(value="Alice")
        name2 = Name(value="Alice")
        assert name1 == name2

    def test_different_objects_are_not_equal(self):
        name1 = Name(value="Alice")
        name2 = Name(value="Bob")
        assert name1 != name2

    def test_is_frozen(self):
        name = Name(value="Alice")
        try:
            name.value = "Bob"
            assert False, "Should not reach here"
        except AttributeError:
            pass
