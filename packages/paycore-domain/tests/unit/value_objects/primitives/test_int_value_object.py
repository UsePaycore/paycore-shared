from dataclasses import dataclass

from paycore_domain.value_objects.primitives import IntValueObject


@dataclass(frozen=True)
class Age(IntValueObject):
    pass


class TestIntValueObject:
    def test_stores_value(self):
        age = Age(value=30)
        assert age.value == 30

    def test_coerces_string_to_int(self):
        age = Age(value="42")
        assert age.value == 42
        assert isinstance(age.value, int)

    def test_int_conversion(self):
        age = Age(value=30)
        assert int(age) == 30

    def test_str_returns_string_representation(self):
        age = Age(value=30)
        assert str(age) == "30"

    def test_repr_includes_class_name(self):
        age = Age(value=30)
        assert "Age" in repr(age)

    def test_less_than(self):
        assert Age(value=20) < Age(value=30)

    def test_less_than_or_equal(self):
        assert Age(value=20) <= Age(value=30)
        assert Age(value=30) <= Age(value=30)

    def test_greater_than(self):
        assert Age(value=30) > Age(value=20)

    def test_greater_than_or_equal(self):
        assert Age(value=30) >= Age(value=20)
        assert Age(value=30) >= Age(value=30)

    def test_equal_objects_are_equal(self):
        assert Age(value=30) == Age(value=30)

    def test_different_objects_are_not_equal(self):
        assert Age(value=30) != Age(value=25)
