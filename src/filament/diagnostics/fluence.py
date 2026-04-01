from __future__ import annotations
import numpy as np

def fluence_rt(intensity_rt, dt):
    return np.trapz(intensity_rt, dx=dt, axis=1)
