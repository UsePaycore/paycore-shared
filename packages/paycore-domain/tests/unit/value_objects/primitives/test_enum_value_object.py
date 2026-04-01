from dataclasses import dataclass
from enum import Enum

from paycore_domain.value_objects.primitives import EnumValueObject


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


@dataclass(frozen=True)
class FavoriteColor(EnumValueObject):
    value: Color


class TestEnumValueObject:
    def test_stores_enum_value(self):
        color = FavoriteColor(value=Color.RED)
        assert color.value == Color.RED

    def test_str_returns_enum_value(self):
        color = FavoriteColor(value=Color.RED)
        assert str(color) == "red"

    def test_repr_includes_class_name(self):
        color = FavoriteColor(value=Color.RED)
        assert "FavoriteColor" in repr(color)

    def test_name_property(self):
        color = FavoriteColor(value=Color.GREEN)
        assert color.name == "GREEN"

    def test_equals_method_with_matching_enum(self):
        color = FavoriteColor(value=Color.RED)
        assert color.equals(Color.RED) is True

    def test_equals_method_with_non_matching_enum(self):
        color = FavoriteColor(value=Color.RED)
        assert color.equals(Color.BLUE) is False

    def test_equal_objects_are_equal(self):
        assert FavoriteColor(value=Color.RED) == FavoriteColor(value=Color.RED)

    def test_different_objects_are_not_equal(self):
        assert FavoriteColor(value=Color.RED) != FavoriteColor(value=Color.BLUE)
