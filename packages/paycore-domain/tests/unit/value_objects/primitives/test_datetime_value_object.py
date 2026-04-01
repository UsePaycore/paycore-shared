from dataclasses import dataclass
from datetime import UTC, date, datetime

from paycore_domain.value_objects.primitives import DateTimeValueObject


@dataclass(frozen=True)
class CreatedAt(DateTimeValueObject):
    pass


class TestDateTimeValueObject:
    def test_stores_datetime_value(self):
        dt = datetime(2026, 3, 30, 12, 0, 0)
        created = CreatedAt(value=dt)
        assert created.value == dt

    def test_coerces_iso_string_to_datetime(self):
        created = CreatedAt(value="2026-03-30T12:00:00")
        assert created.value == datetime(2026, 3, 30, 12, 0, 0)
        assert isinstance(created.value, datetime)

    def test_str_returns_iso_format(self):
        dt = datetime(2026, 3, 30, 12, 0, 0)
        created = CreatedAt(value=dt)
        assert str(created) == "2026-03-30T12:00:00"

    def test_repr_includes_class_name(self):
        dt = datetime(2026, 3, 30, 12, 0, 0)
        created = CreatedAt(value=dt)
        assert "CreatedAt" in repr(created)

    def test_less_than(self):
        earlier = CreatedAt(value=datetime(2026, 1, 1))
        later = CreatedAt(value=datetime(2026, 6, 1))
        assert earlier < later

    def test_less_than_or_equal(self):
        dt = datetime(2026, 1, 1)
        assert CreatedAt(value=dt) <= CreatedAt(value=dt)

    def test_greater_than(self):
        earlier = CreatedAt(value=datetime(2026, 1, 1))
        later = CreatedAt(value=datetime(2026, 6, 1))
        assert later > earlier

    def test_greater_than_or_equal(self):
        dt = datetime(2026, 1, 1)
        assert CreatedAt(value=dt) >= CreatedAt(value=dt)

    def test_date_property(self):
        dt = datetime(2026, 3, 30, 12, 0, 0)
        created = CreatedAt(value=dt)
        assert created.date == date(2026, 3, 30)

    def test_year_property(self):
        created = CreatedAt(value=datetime(2026, 3, 30))
        assert created.year == 2026

    def test_month_property(self):
        created = CreatedAt(value=datetime(2026, 3, 30))
        assert created.month == 3

    def test_day_property(self):
        created = CreatedAt(value=datetime(2026, 3, 30))
        assert created.day == 30

    def test_now_returns_current_time(self):
        before = datetime.now(UTC)
        created = CreatedAt.now()
        after = datetime.now(UTC)
        assert before <= created.value <= after

    def test_equal_objects_are_equal(self):
        dt = datetime(2026, 3, 30, 12, 0, 0)
        assert CreatedAt(value=dt) == CreatedAt(value=dt)
