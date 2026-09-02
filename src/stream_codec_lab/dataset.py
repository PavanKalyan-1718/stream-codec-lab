"""Deterministic event data that resembles a compact analytics stream."""

from __future__ import annotations

import json
import random
from datetime import datetime, timedelta, timezone


def generate_events(count: int, seed: int = 42) -> bytes:
    """Return newline-delimited JSON with repeated dimensions and noisy metrics."""
    if count < 1:
        raise ValueError("count must be positive")

    randomizer = random.Random(seed)
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    regions = ("us-east-1", "us-west-2", "eu-west-1")
    services = ("checkout", "catalog", "search", "payments")
    lines = []
    for index in range(count):
        event = {
            "timestamp": (start + timedelta(milliseconds=index * 25)).isoformat(),
            "region": regions[index % len(regions)],
            "service": services[index % len(services)],
            "status": 200 if index % 31 else 429,
            "latency_ms": round(randomizer.lognormvariate(2.8, 0.35), 2),
            "request_id": f"req-{index:09d}",
        }
        lines.append(json.dumps(event, separators=(",", ":"), sort_keys=True))
    return ("\n".join(lines) + "\n").encode("utf-8")

