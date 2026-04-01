from __future__ import annotations
import numpy as np


def omega_kernel(t, omega_r, gamma_r):
    tp = np.maximum(t, 0.0)
    k = np.exp(-gamma_r * tp) * np.sin(omega_r * tp)
    k[t < 0.0] = 0.0
    return k


def q_response(intensity_rt, dt, t, n_r, n0, chi_l, omega_r, gamma_r):
    """Causal Raman response via FFT convolution along time axis."""
    kern = omega_kernel(t, omega_r, gamma_r)
    n = intensity_rt.shape[1]
    nfft = 1 << (2 * n - 1).bit_length()
    Ik = np.fft.fft(intensity_rt, n=nfft, axis=1)
    Kk = np.fft.fft(kern[None, :], n=nfft, axis=1)
    conv = np.fft.ifft(Ik * Kk, axis=1)[:, :n].real * dt
    return -(n_r / (n0 * 2 * np.pi * chi_l)) * conv
