from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4

from paycore_domain.entities import AggregateRoot
from paycore_domain.events import DomainEvent
from paycore_domain.value_objects import EntityId


@dataclass(frozen=True, kw_only=True)
class FakeEvent(DomainEvent):
    name: str

    @staticmethod
    def event_name() -> str:
        return "fake.event.created"

    def to_primitives(self) -> Dict[str, Any]:
        return {"name": self.name}

    @classmethod
    def from_primitives(
        cls,
        aggregate_id: UUID,
        event_id: UUID,
        occurred_at: datetime,
        body: Dict[str, Any],
    ) -> "FakeEvent":
        return cls(
            aggregate_id=aggregate_id,
            event_id=event_id,
            occurred_at=occurred_at,
            name=body["name"],
        )


class ConcreteAggregate(AggregateRoot[EntityId]):
    pass


class TestAggregateRoot:
    def test_starts_with_no_domain_events(self):
        aggregate = ConcreteAggregate(id=EntityId.generate())
        assert aggregate.domain_events == []

    def test_add_domain_event(self):
        aggregate = ConcreteAggregate(id=EntityId.generate())
        event = FakeEvent(aggregate_id=uuid4(), name="test")
        aggregate.add_domain_event(event)
        assert len(aggregate.domain_events) == 1
        assert aggregate.domain_events[0] == event

    def test_domain_events_returns_copy(self):
        aggregate = ConcreteAggregate(id=EntityId.generate())
        event = FakeEvent(aggregate_id=uuid4(), name="test")
        aggregate.add_domain_event(event)
        events = aggregate.domain_events
        events.clear()
        assert len(aggregate.domain_events) == 1

    def test_clear_domain_events(self):
        aggregate = ConcreteAggregate(id=EntityId.generate())
        aggregate.add_domain_event(FakeEvent(aggregate_id=uuid4(), name="test"))
        aggregate.clear_domain_events()
        assert aggregate.domain_events == []

    def test_pop_domain_events_returns_events_and_clears(self):
        aggregate = ConcreteAggregate(id=EntityId.generate())
        event = FakeEvent(aggregate_id=uuid4(), name="test")
        aggregate.add_domain_event(event)
        popped = aggregate.pop_domain_events()
        assert len(popped) == 1
        assert popped[0] == event
        assert aggregate.domain_events == []

    def test_multiple_events(self):
        aggregate = ConcreteAggregate(id=EntityId.generate())
        event1 = FakeEvent(aggregate_id=uuid4(), name="first")
        event2 = FakeEvent(aggregate_id=uuid4(), name="second")
        aggregate.add_domain_event(event1)
        aggregate.add_domain_event(event2)
        assert len(aggregate.domain_events) == 2
