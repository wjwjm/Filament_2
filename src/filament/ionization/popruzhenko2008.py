"""Popruzhenko 2008 arbitrary-Keldysh ionization rate backend.

Scope note:
- Atomic / positive ion, linear polarization, s-state, single-active-electron framework.
- This is NOT automatically a molecular Popruzhenko model.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy import special
from filament.constants import EV

@dataclass
class PopruzhenkoSpeciesParams:
    ip_ev: float
    Z: float
    n_star: float


def rate_popruzhenko(I_SI, species_params: PopruzhenkoSpeciesParams, omega0_SI):
    I = np.asarray(I_SI, dtype=float)
    I_cm2 = np.maximum(I * 1e-4, 1e-30)
    F = np.sqrt(I_cm2 / 3.509e16)
    Ip_au = (species_params.ip_ev * EV) / 4.3597447222071e-18
    gamma = omega0_SI * np.sqrt(2 * Ip_au) / np.maximum(F * 4.134137e16, 1e-30)
    g = 1.5 / np.maximum(gamma, 1e-30) * ((1 + 1 / (2 * gamma**2)) * np.arcsinh(gamma) - np.sqrt(1 + gamma**2) / (2 * gamma))
    c1 = np.arcsinh(gamma) - gamma / np.sqrt(1 + gamma**2)
    K0 = Ip_au / max(omega0_SI / 4.134137e16, 1e-12)
    nth = K0 * (1 + 1 / (2 * np.maximum(gamma**2, 1e-30)))
    x = np.sqrt(np.clip(nth - np.floor(nth), 0, 1))
    daw = special.dawsn(x)
    C2 = 2 ** (2 * species_params.n_star - 2) / np.maximum(special.gamma(species_params.n_star + 1), 1e-30) ** 2
    w_sr = 2 * C2 * np.maximum(F, 1e-30) * daw * np.exp(np.clip(-2 * g / (3 * np.maximum(F, 1e-30)) - 2 * c1 * (nth - np.floor(nth)), -700, 50))
    Q = (2 / np.maximum(F, 1e-30)) ** (2 * species_params.n_star) * (1 + 2 * np.exp(-1) / np.maximum(gamma, 1e-30)) ** (-2 * species_params.n_star)
    return np.nan_to_num(Q * w_sr * 4.134137e16, nan=0.0, posinf=1e40)
