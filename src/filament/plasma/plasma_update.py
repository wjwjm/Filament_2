from __future__ import annotations
import numpy as np
from .rk4 import rk4_step

def update_species_density_rk4(nj, nj0, dt, rate_func, intensity):
    def rhs(n):
        return rate_func(intensity) * (nj0 - n)
    out = rk4_step(nj, dt, rhs)
    return np.clip(out, 0.0, nj0)
