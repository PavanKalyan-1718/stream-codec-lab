# Stream Codec Lab

> Reproducible compression experiments for data-processing workloads.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![CI](https://img.shields.io/github/actions/workflow/status/PavanKalyan-1718/stream-codec-lab/test.yml?label=tests)
![License](https://img.shields.io/badge/license-MIT-22c55e)

`stream-codec-lab` is a focused benchmark harness for answering a practical systems question: **how do compression ratio and throughput change for a realistic event stream?** It generates deterministic newline-delimited JSON, validates lossless round trips, and measures compression and decompression throughput across standard codecs.

## Why this project

Modern analytics and distributed systems spend substantial time moving data. Compression decisions influence storage cost, network pressure, memory use, and end-to-end query latency. This repository creates an auditable CPU baseline before evaluating hardware-accelerated paths such as CUDA/nvCOMP.

## Run it

```bash
git clone https://github.com/PavanKalyan-1718/stream-codec-lab.git
cd stream-codec-lab
python3 -m venv .venv && source .venv/bin/activate
pip install -e . pytest
stream-codec-bench --events 50000 --iterations 3 --output benchmarks/latest.json
pytest -q
```

The report includes input size, compressed size, compression ratio, compression throughput, and decompression throughput.

## Design notes

- **Fair inputs:** every codec receives identical seeded data.
- **Correctness first:** a lossless round trip is verified before any metric is returned.
- **Reproducible outputs:** JSON reports are easy to compare in CI or a future performance dashboard.
- **Honest scope:** this release is a CPU baseline. GPU acceleration is planned, not claimed.

## Roadmap

- Add Parquet/Arrow column benchmarks and dictionary encoding experiments.
- Add Zstandard and LZ4 adapters with pinned dependencies.
- Compare GPU acceleration with NVIDIA nvCOMP where a CUDA environment is available.
- Add result visualizations and a performance-regression threshold in CI.

## Related skills

Python | algorithms | data processing | ETL | compression | benchmark design | GitHub Actions

## License

MIT
