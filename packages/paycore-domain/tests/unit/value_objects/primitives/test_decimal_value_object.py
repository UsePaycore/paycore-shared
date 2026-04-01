from dataclasses import dataclass
from decimal import Decimal

from paycore_domain.value_objects.primitives import DecimalValueObject


@dataclass(frozen=True)
class Price(DecimalValueObject):
    pass


class TestDecimalValueObject:
    def test_stores_decimal_value(self):
        price = Price(value=Decimal("19.99"))
        assert price.value == Decimal("19.99")

    def test_coerces_float_to_decimal(self):
        price = Price(value=19.99)
        assert isinstance(price.value, Decimal)

    def test_coerces_int_to_decimal(self):
        price = Price(value=20)
        assert isinstance(price.value, Decimal)
        assert price.value == Decimal("20")

    def test_float_conversion(self):
        price = Price(value=Decimal("19.99"))
        assert float(price) == 19.99

    def test_str_returns_string_representation(self):
        price = Price(value=Decimal("19.99"))
        assert str(price) == "19.99"

    def test_repr_includes_class_name(self):
        price = Price(value=Decimal("19.99"))
        assert "Price" in repr(price)

    def test_less_than(self):
        assert Price(value=Decimal("10")) < Price(value=Decimal("20"))

    def test_less_than_or_equal(self):
        assert Price(value=Decimal("10")) <= Price(value=Decimal("20"))
        assert Price(value=Decimal("10")) <= Price(value=Decimal("10"))

    def test_greater_than(self):
        assert Price(value=Decimal("20")) > Price(value=Decimal("10"))

    def test_greater_than_or_equal(self):
        assert Price(value=Decimal("20")) >= Price(value=Decimal("10"))
        assert Price(value=Decimal("20")) >= Price(value=Decimal("20"))

    def test_addition(self):
        result = Price(value=Decimal("10")) + Price(value=Decimal("5"))
        assert result == Decimal("15")

    def test_subtraction(self):
        result = Price(value=Decimal("10")) - Price(value=Decimal("3"))
        assert result == Decimal("7")

    def test_multiplication(self):
        result = Price(value=Decimal("10")) * Price(value=Decimal("3"))
        assert result == Decimal("30")

    def test_division(self):
        result = Price(value=Decimal("10")) / Price(value=Decimal("4"))
        assert result == Decimal("2.5")

    def test_equal_objects_are_equal(self):
        assert Price(value=Decimal("19.99")) == Price(value=Decimal("19.99"))

    def test_different_objects_are_not_equal(self):
        assert Price(value=Decimal("19.99")) != Price(value=Decimal("29.99"))
