"""Command-line compression benchmark with reproducible measurements."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from .codecs import Codec, available_codecs
from .dataset import generate_events


@dataclass(frozen=True)
class BenchmarkResult:
    codec: str
    input_bytes: int
    compressed_bytes: int
    compression_ratio: float
    compress_mib_per_second: float
    decompress_mib_per_second: float


def _throughput(bytes_processed: int, seconds: float) -> float:
    return round(bytes_processed / (1024 * 1024) / seconds, 2)


def benchmark_codec(codec: Codec, payload: bytes, iterations: int = 3) -> BenchmarkResult:
    """Benchmark a codec and verify every round trip before reporting it."""
    if iterations < 1:
        raise ValueError("iterations must be positive")

    compressed = codec.compress(payload)
    if codec.decompress(compressed) != payload:
        raise RuntimeError(f"{codec.name} failed round-trip verification")

    compress_start = time.perf_counter()
    for _ in range(iterations):
        compressed = codec.compress(payload)
    compress_seconds = time.perf_counter() - compress_start

    decompress_start = time.perf_counter()
    for _ in range(iterations):
        codec.decompress(compressed)
    decompress_seconds = time.perf_counter() - decompress_start

    return BenchmarkResult(
        codec=codec.name,
        input_bytes=len(payload),
        compressed_bytes=len(compressed),
        compression_ratio=round(len(payload) / len(compressed), 3),
        compress_mib_per_second=_throughput(len(payload) * iterations, compress_seconds),
        decompress_mib_per_second=_throughput(len(payload) * iterations, decompress_seconds),
    )


def run_benchmark(events: int, iterations: int) -> list[BenchmarkResult]:
    payload = generate_events(events)
    return [benchmark_codec(codec, payload, iterations) for codec in available_codecs()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark standard-library compression codecs.")
    parser.add_argument("--events", type=int, default=50_000)
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--output", type=Path, help="Optional JSON results path")
    args = parser.parse_args()

    results = run_benchmark(args.events, args.iterations)
    rendered = json.dumps([asdict(result) for result in results], indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

