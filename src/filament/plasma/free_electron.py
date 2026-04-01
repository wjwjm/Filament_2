from __future__ import annotations
import numpy as np

def p_free(A, omega0, omega_p2, nu_e=0.0):
    return -(omega_p2 / (omega0**2)) * (1.0 - 1j * nu_e / omega0) * A / (4*np.pi)
