from __future__ import annotations
import numpy as np

def pulse_energy(intensity_rt, r, dt):
    radial = 2 * np.pi * np.trapz(intensity_rt * r[:, None], x=r, axis=0)
    return np.trapz(radial, dx=dt)
