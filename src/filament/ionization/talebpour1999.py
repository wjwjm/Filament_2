"""Talebpour 1999 Appendix-A style PPT scaffold for molecules (N2/O2)."""
from __future__ import annotations
import numpy as np
from scipy import special
from filament.constants import EPS0, C, EV


def _intensity_to_field_au(I_w_m2):
    I_w_cm2 = I_w_m2 * 1e-4
    return np.sqrt(np.clip(I_w_cm2, 0.0, None) / 3.509e16)


def rate_talebpour(I_SI, species, omega0_SI):
    """Cycle-averaged molecular PPT rate, numerically stabilized.

    Notes:
    - Uses Talebpour semi-empirical species parameters (Zeff, l=0,m=0).
    - Keeps PPT auxiliary structure g(gamma), prefactors, and Dawson usage.
    """
    I = np.asarray(I_SI, dtype=float)
    F_au = np.maximum(_intensity_to_field_au(I), 1e-30)
    ip_au = (species.ip_ev * EV) / (4.3597447222071e-18)
    gamma = omega0_SI * np.sqrt(2.0 * ip_au) / np.maximum(F_au * 4.134137e16, 1e-30)
    g = ((1 + 2 * gamma**2) * np.arcsinh(gamma) - gamma * np.sqrt(1 + gamma**2)) / (2 * gamma**3 + 1e-30)
    expo = -2.0 * (2 * ip_au) ** 1.5 * g / (3 * np.maximum(F_au, 1e-30))
    expo = np.clip(expo, -700, 80)
    daws = special.dawsn(np.sqrt(np.clip(gamma, 0, 1e6)))
    pref = np.maximum(species.z_eff, 1e-6) * (1 + daws**2) * np.maximum(F_au, 1e-30)
    rate_au = pref * np.exp(expo)
    return np.nan_to_num(rate_au * 4.134137e16, nan=0.0, posinf=1e40)
