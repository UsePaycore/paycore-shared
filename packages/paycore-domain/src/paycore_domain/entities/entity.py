from abc import ABC
from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from paycore_domain.value_objects.primitives import ValueObject

TId = TypeVar("TId", bound=ValueObject)


class Entity(ABC, Generic[TId]):
    def __init__(self, id: TId) -> None:
        self._id = id
        self._created_at: datetime = datetime.now(UTC)
        self._updated_at: datetime = datetime.now(UTC)

    @property
    def id(self) -> TId:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def _update_timestamp(self) -> None:
        self._updated_at = datetime.now(UTC)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entity):
            return False
        return bool(self._id == other._id)

    def __hash__(self) -> int:
        return hash(self._id)
