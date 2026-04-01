from __future__ import annotations
import numpy as np

def thin_lens_phase(r, k0, f_m):
    return np.exp(-1j * k0 * r[:, None] ** 2 / (2 * f_m))
