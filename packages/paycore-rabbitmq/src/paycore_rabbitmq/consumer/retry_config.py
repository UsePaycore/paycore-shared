from dataclasses import dataclass


@dataclass(frozen=True)
class RetryConfig:
    max_retries: int = 3
    retry_ttl_ms: int = 5000
    backoff_multiplier: int = 5
    dead_letter_ttl_ms: int = 86400000
