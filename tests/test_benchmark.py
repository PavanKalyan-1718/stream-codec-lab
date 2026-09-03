from stream_codec_lab.benchmark import benchmark_codec, run_benchmark
from stream_codec_lab.codecs import available_codecs
from stream_codec_lab.dataset import WORKLOADS, generate_events


def test_event_generator_is_deterministic() -> None:
    assert generate_events(10) == generate_events(10)


def test_workloads_are_deterministic_and_distinct() -> None:
    repetitive = generate_events(10, workload="repetitive")
    high_cardinality = generate_events(10, workload="high-cardinality")
    assert generate_events(10, workload="high-cardinality") == high_cardinality
    assert repetitive != high_cardinality
    assert len(high_cardinality) > len(repetitive)


def test_rejects_unknown_workload() -> None:
    try:
        generate_events(10, workload="unknown")
    except ValueError as error:
        assert "workload must be one of" in str(error)
    else:
        raise AssertionError("unknown workload should fail")


def test_all_codecs_round_trip() -> None:
    payload = generate_events(100)
    for codec in available_codecs():
        assert codec.decompress(codec.compress(payload)) == payload


def test_benchmark_reports_positive_metrics() -> None:
    result = benchmark_codec(available_codecs()[0], generate_events(100), iterations=1)
    assert result.compression_ratio > 1
    assert result.compress_mib_per_second > 0
    assert result.decompress_mib_per_second > 0


def test_run_benchmark_covers_all_codecs() -> None:
    results = run_benchmark(events=100, iterations=1, workload="high-cardinality")
    assert len(results) == len(available_codecs())
    assert {result.workload for result in results} == {"high-cardinality"}
