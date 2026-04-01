from __future__ import annotations
import numpy as np

try:
    import cupy as cp
    xp = cp
    CUPY_AVAILABLE = True
except Exception:
    cp = None
    xp = np
    CUPY_AVAILABLE = False


def get_xp(use_gpu: bool = True):
    return cp if (use_gpu and CUPY_AVAILABLE) else np


def asnumpy(arr):
    if CUPY_AVAILABLE and isinstance(arr, cp.ndarray):
        return cp.asnumpy(arr)
    return arr


def to_device(arr, use_gpu: bool = True):
    target = get_xp(use_gpu)
    if target is np:
        return np.asarray(arr)
    return cp.asarray(arr)
