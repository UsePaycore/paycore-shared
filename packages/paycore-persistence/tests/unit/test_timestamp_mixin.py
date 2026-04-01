from datetime import datetime

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from paycore_persistence import Base, TimestampMixin


class TimestampedModel(Base, TimestampMixin):
    __tablename__ = "timestamped_test"

    from sqlalchemy import Column, Integer

    id = Column(Integer, primary_key=True, autoincrement=True)


class TestTimestampMixin:
    def _create_session(self) -> Session:
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        return Session(engine)

    def test_model_has_created_at_column(self):
        columns = {c.name for c in inspect(TimestampedModel).columns}
        assert "created_at" in columns

    def test_model_has_updated_at_column(self):
        columns = {c.name for c in inspect(TimestampedModel).columns}
        assert "updated_at" in columns

    def test_created_at_is_set_on_insert(self):
        session = self._create_session()
        record = TimestampedModel()
        session.add(record)
        session.commit()
        session.refresh(record)
        assert record.created_at is not None
        assert isinstance(record.created_at, datetime)
        session.close()

    def test_updated_at_is_set_on_insert(self):
        session = self._create_session()
        record = TimestampedModel()
        session.add(record)
        session.commit()
        session.refresh(record)
        assert record.updated_at is not None
        assert isinstance(record.updated_at, datetime)
        session.close()
