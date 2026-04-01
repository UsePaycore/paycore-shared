from dataclasses import dataclass

from paycore_domain.value_objects.primitives import BooleanValueObject


@dataclass(frozen=True)
class IsActive(BooleanValueObject):
    pass


class TestBooleanValueObject:
    def test_stores_true_value(self):
        active = IsActive(value=True)
        assert active.value is True

    def test_stores_false_value(self):
        active = IsActive(value=False)
        assert active.value is False

    def test_coerces_truthy_to_bool(self):
        active = IsActive(value=1)
        assert active.value is True
        assert isinstance(active.value, bool)

    def test_coerces_falsy_to_bool(self):
        active = IsActive(value=0)
        assert active.value is False
        assert isinstance(active.value, bool)

    def test_bool_conversion(self):
        assert bool(IsActive(value=True)) is True
        assert bool(IsActive(value=False)) is False

    def test_str_returns_lowercase(self):
        assert str(IsActive(value=True)) == "true"
        assert str(IsActive(value=False)) == "false"

    def test_repr_includes_class_name(self):
        assert "IsActive" in repr(IsActive(value=True))

    def test_is_true(self):
        assert IsActive(value=True).is_true() is True
        assert IsActive(value=False).is_true() is False

    def test_is_false(self):
        assert IsActive(value=False).is_false() is True
        assert IsActive(value=True).is_false() is False

    def test_equal_objects_are_equal(self):
        assert IsActive(value=True) == IsActive(value=True)

    def test_different_objects_are_not_equal(self):
        assert IsActive(value=True) != IsActive(value=False)
