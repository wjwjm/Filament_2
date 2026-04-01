from __future__ import annotations
import numpy as np

def p_ion(A, dn_dt, ionization_energy_j, n0, omega0):
    denom = np.maximum(np.abs(A)**2, 1e-30)
    return 2j * n0 * omega0 * A * (ionization_energy_j * dn_dt) / denom
