"""Codec adapters with one consistent interface for fair comparisons."""

from __future__ import annotations

import bz2
import gzip
import lzma
import zlib
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Codec:
    name: str
    compress: Callable[[bytes], bytes]
    decompress: Callable[[bytes], bytes]


def available_codecs() -> tuple[Codec, ...]:
    return (
        Codec("gzip-6", lambda payload: gzip.compress(payload, compresslevel=6), gzip.decompress),
        Codec("zlib-6", lambda payload: zlib.compress(payload, level=6), zlib.decompress),
        Codec("bz2-9", lambda payload: bz2.compress(payload, compresslevel=9), bz2.decompress),
        Codec("lzma-6", lambda payload: lzma.compress(payload, preset=6), lzma.decompress),
    )

