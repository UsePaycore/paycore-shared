from dataclasses import dataclass
from datetime import date

from paycore_domain.value_objects.primitives import DateValueObject


@dataclass(frozen=True)
class BirthDate(DateValueObject):
    pass


class TestDateValueObject:
    def test_stores_date_value(self):
        d = date(2026, 3, 30)
        bd = BirthDate(value=d)
        assert bd.value == d

    def test_coerces_iso_string_to_date(self):
        bd = BirthDate(value="2026-03-30")
        assert bd.value == date(2026, 3, 30)
        assert isinstance(bd.value, date)

    def test_str_returns_iso_format(self):
        bd = BirthDate(value=date(2026, 3, 30))
        assert str(bd) == "2026-03-30"

    def test_repr_includes_class_name(self):
        bd = BirthDate(value=date(2026, 3, 30))
        assert "BirthDate" in repr(bd)

    def test_less_than(self):
        assert BirthDate(value=date(2020, 1, 1)) < BirthDate(value=date(2021, 1, 1))

    def test_less_than_or_equal(self):
        assert BirthDate(value=date(2020, 1, 1)) <= BirthDate(value=date(2021, 1, 1))
        assert BirthDate(value=date(2020, 1, 1)) <= BirthDate(value=date(2020, 1, 1))

    def test_greater_than(self):
        assert BirthDate(value=date(2021, 1, 1)) > BirthDate(value=date(2020, 1, 1))

    def test_greater_than_or_equal(self):
        assert BirthDate(value=date(2021, 1, 1)) >= BirthDate(value=date(2020, 1, 1))
        assert BirthDate(value=date(2020, 1, 1)) >= BirthDate(value=date(2020, 1, 1))

    def test_year_property(self):
        bd = BirthDate(value=date(2026, 3, 30))
        assert bd.year == 2026

    def test_month_property(self):
        bd = BirthDate(value=date(2026, 3, 30))
        assert bd.month == 3

    def test_day_property(self):
        bd = BirthDate(value=date(2026, 3, 30))
        assert bd.day == 30

    def test_equal_objects_are_equal(self):
        d = date(2026, 3, 30)
        assert BirthDate(value=d) == BirthDate(value=d)
