import json
from typing import Any, Dict
from unittest.mock import MagicMock

import pika
from pika.spec import Basic, BasicProperties

from paycore_rabbitmq.consumer.consumer_with_retry import (
    RabbitMqConsumerWithRetry,
    RetryConfig,
)


class FakeConsumer(RabbitMqConsumerWithRetry):
    def __init__(self, connection, retry_config=None):
        super().__init__(
            connection=connection,
            exchange_name="test_exchange",
            queue_name="test_queue",
            routing_keys=["test.event"],
            retry_config=retry_config,
        )
        self.handled_events = []

    def handle_event(self, event_name: str, message: Dict[str, Any]) -> None:
        self.handled_events.append((event_name, message))


class FailingConsumer(RabbitMqConsumerWithRetry):
    def __init__(self, connection, retry_config=None):
        super().__init__(
            connection=connection,
            exchange_name="test_exchange",
            queue_name="test_queue",
            routing_keys=["test.event"],
            retry_config=retry_config,
        )

    def handle_event(self, event_name: str, message: Dict[str, Any]) -> None:
        raise RuntimeError("Processing failed")


def _create_mock_connection():
    connection = MagicMock()
    channel = MagicMock()
    connection.channel.return_value = channel
    return connection, channel


def _create_method(routing_key="test.event"):
    method = MagicMock(spec=Basic.Deliver)
    method.routing_key = routing_key
    method.delivery_tag = 1
    return method


def _create_properties(headers=None, message_id="msg-123"):
    props = MagicMock(spec=BasicProperties)
    props.headers = headers
    props.message_id = message_id
    return props


class TestExponentialBackoff:
    def test_default_config_has_backoff_multiplier(self):
        config = RetryConfig()
        assert config.backoff_multiplier == 5

    def test_calculate_retry_ttl_first_retry(self):
        connection, _ = _create_mock_connection()
        consumer = FakeConsumer(connection, RetryConfig(retry_ttl_ms=5000, backoff_multiplier=5))
        assert consumer._calculate_retry_ttl(0) == 5000

    def test_calculate_retry_ttl_second_retry(self):
        connection, _ = _create_mock_connection()
        consumer = FakeConsumer(connection, RetryConfig(retry_ttl_ms=5000, backoff_multiplier=5))
        assert consumer._calculate_retry_ttl(1) == 25000

    def test_calculate_retry_ttl_third_retry(self):
        connection, _ = _create_mock_connection()
        consumer = FakeConsumer(connection, RetryConfig(retry_ttl_ms=5000, backoff_multiplier=5))
        assert consumer._calculate_retry_ttl(2) == 125000

    def test_retry_message_includes_expiration_header(self):
        connection, channel = _create_mock_connection()
        consumer = FailingConsumer(
            connection,
            RetryConfig(retry_ttl_ms=5000, backoff_multiplier=5, max_retries=3),
        )

        body = json.dumps({"event_name": "test.event"}).encode()
        method = _create_method()
        properties = _create_properties()

        consumer._on_message(channel, method, properties, body)

        publish_call = channel.basic_publish.call_args
        retry_properties = publish_call.kwargs["properties"]
        assert retry_properties.expiration == "5000"

    def test_second_retry_has_longer_expiration(self):
        connection, channel = _create_mock_connection()
        consumer = FailingConsumer(
            connection,
            RetryConfig(retry_ttl_ms=5000, backoff_multiplier=5, max_retries=3),
        )

        body = json.dumps({"event_name": "test.event"}).encode()
        method = _create_method()
        properties = _create_properties(headers={"x-retry-count": 1})

        consumer._on_message(channel, method, properties, body)

        publish_call = channel.basic_publish.call_args
        retry_properties = publish_call.kwargs["properties"]
        assert retry_properties.expiration == "25000"

    def test_third_retry_has_longest_expiration(self):
        connection, channel = _create_mock_connection()
        consumer = FailingConsumer(
            connection,
            RetryConfig(retry_ttl_ms=5000, backoff_multiplier=5, max_retries=3),
        )

        body = json.dumps({"event_name": "test.event"}).encode()
        method = _create_method()
        properties = _create_properties(headers={"x-retry-count": 2})

        consumer._on_message(channel, method, properties, body)

        publish_call = channel.basic_publish.call_args
        retry_properties = publish_call.kwargs["properties"]
        assert retry_properties.expiration == "125000"

    def test_max_retries_exceeded_sends_to_dead_letter(self):
        connection, channel = _create_mock_connection()
        consumer = FailingConsumer(
            connection,
            RetryConfig(retry_ttl_ms=5000, backoff_multiplier=5, max_retries=3),
        )

        body = json.dumps({"event_name": "test.event"}).encode()
        method = _create_method()
        properties = _create_properties(headers={"x-retry-count": 3})

        consumer._on_message(channel, method, properties, body)

        publish_call = channel.basic_publish.call_args
        assert publish_call.kwargs["exchange"] == "test_exchange.dead_letter"

    def test_setup_retry_queue_without_message_ttl(self):
        connection, channel = _create_mock_connection()
        consumer = FakeConsumer(connection)

        consumer._setup_retry_infrastructure()

        connection.declare_queue_with_dlx.assert_called_once_with(
            queue_name="test_queue.retry",
            dead_letter_exchange="test_exchange",
        )

    def test_setup_retry_recreates_queue_on_precondition_failed(self):
        connection, channel = _create_mock_connection()
        consumer = FakeConsumer(connection)

        connection.declare_queue_with_dlx.side_effect = [
            pika.exceptions.ChannelClosedByBroker(406, "PRECONDITION_FAILED"),
            None,
        ]

        consumer._setup_retry_infrastructure()

        connection._reconnect.assert_called_once()
        channel.queue_delete.assert_called_once_with(queue="test_queue.retry")
        assert connection.declare_queue_with_dlx.call_count == 2

    def test_setup_retry_raises_non_precondition_errors(self):
        connection, channel = _create_mock_connection()
        consumer = FakeConsumer(connection)

        connection.declare_queue_with_dlx.side_effect = (
            pika.exceptions.ChannelClosedByBroker(500, "INTERNAL_ERROR")
        )

        try:
            consumer._setup_retry_infrastructure()
            assert False, "Should have raised"
        except pika.exceptions.ChannelClosedByBroker as e:
            assert e.reply_code == 500
