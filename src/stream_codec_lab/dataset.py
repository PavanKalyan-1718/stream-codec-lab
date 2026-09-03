"""Deterministic event data that models contrasting analytics-stream shapes."""

from __future__ import annotations

import json
import random
import string
from datetime import datetime, timedelta, timezone

WORKLOADS = ("repetitive", "high-cardinality")


def _random_token(randomizer: random.Random, length: int = 20) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(randomizer.choices(alphabet, k=length))


def generate_events(count: int, seed: int = 42, workload: str = "repetitive") -> bytes:
    """Return NDJSON for a repeated-dimension or high-cardinality event workload."""
    if count < 1:
        raise ValueError("count must be positive")
    if workload not in WORKLOADS:
        raise ValueError(f"workload must be one of: {', '.join(WORKLOADS)}")

    randomizer = random.Random(seed)
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    regions = ("us-east-1", "us-west-2", "eu-west-1")
    services = ("checkout", "catalog", "search", "payments")
    lines = []
    for index in range(count):
        event: dict[str, object] = {
            "timestamp": (start + timedelta(milliseconds=index * 25)).isoformat(),
            "region": regions[index % len(regions)],
            "service": services[index % len(services)],
            "status": 200 if index % 31 else 429,
            "latency_ms": round(randomizer.lognormvariate(2.8, 0.35), 2),
            "request_id": f"req-{index:09d}",
        }
        if workload == "high-cardinality":
            # Model trace attributes that are difficult for general-purpose codecs to reuse.
            event["session_id"] = _random_token(randomizer, 24)
            event["trace_id"] = _random_token(randomizer, 32)
            event["resource_path"] = f"/objects/{_random_token(randomizer, 16)}"
        lines.append(json.dumps(event, separators=(",", ":"), sort_keys=True))
    return ("\n".join(lines) + "\n").encode("utf-8")
