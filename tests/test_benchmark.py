from stream_codec_lab.benchmark import benchmark_codec, run_benchmark
from stream_codec_lab.codecs import available_codecs
from stream_codec_lab.dataset import generate_events


def test_event_generator_is_deterministic() -> None:
    assert generate_events(10) == generate_events(10)


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
    assert len(run_benchmark(events=100, iterations=1)) == len(available_codecs())

