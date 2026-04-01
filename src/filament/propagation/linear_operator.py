from __future__ import annotations
import numpy as np


def linear_phase_gvd(omega, beta2, dz):
    """Temporal GVD phase operator in frequency domain."""
    return np.exp(-0.5j * beta2 * omega**2 * dz)


def radial_laplacian_axisymmetric(A, r, dr):
    """Axisymmetric Laplacian: d2A/dr2 + (1/r)dA/dr with regularity at r=0."""
    out = np.zeros_like(A, dtype=np.complex128)
    # center: (1/r)dA/dr -> 0; use even symmetry
    out[0, :] = 2.0 * (A[1, :] - A[0, :]) / (dr**2)
    # interior
    rp = r[1:-1, None]
    d2 = (A[2:, :] - 2.0 * A[1:-1, :] + A[:-2, :]) / (dr**2)
    d1 = (A[2:, :] - A[:-2, :]) / (2.0 * dr)
    out[1:-1, :] = d2 + d1 / np.maximum(rp, 1e-30)
    # outer boundary: Sommerfeld-like weak absorbing slope
    out[-1, :] = (A[-2, :] - A[-1, :]) / (dr**2)
    return out


def apply_linear_half_step(A, omega, r, dr, dz, k0, beta2):
    """Half linear step: GVD (spectral in t) + paraxial diffraction (r)."""
    Aw = np.fft.fft(A, axis=1)
    Aw *= linear_phase_gvd(omega, beta2, 0.5 * dz)[None, :]
    A1 = np.fft.ifft(Aw, axis=1)
    lap = radial_laplacian_axisymmetric(A1, r, dr)
    return A1 + 1j * (0.5 * dz) * lap / (2.0 * k0)
