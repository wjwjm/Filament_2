from __future__ import annotations
import numpy as np
from .constants import C, EPS0

def gaussian_pulse_rt(r, t, p_peak_w, tau_fwhm_s, w0_m, n0=1.0):
    t0 = tau_fwhm_s / np.sqrt(2 * np.log(2))
    ir = np.exp(-2 * (r[:, None] ** 2) / (w0_m ** 2))
    it = np.exp(-4 * np.log(2) * (t[None, :] ** 2) / (tau_fwhm_s ** 2))
    intensity = p_peak_w * ir * it / (0.5 * np.pi * w0_m**2)
    amp = np.sqrt(2 * intensity / (n0 * EPS0 * C))
    return amp.astype(np.complex128)
