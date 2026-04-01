from __future__ import annotations
import numpy as np
from filament.diagnostics.intensity import intensity_from_field
from filament.nonlinear.kerr import p_electronic
from filament.nonlinear.raman import q_response
from filament.plasma.free_electron import p_free
from filament.plasma.ionization_damping import p_ion
from filament.constants import E_CHARGE, M_E, EPS0


def strict_inverse_operator(A, omega, omega0):
    """Apply (1 + i/omega0 * d/dt)^(-1) exactly in frequency domain."""
    Aw = np.fft.fft(A, axis=1)
    inv = 1.0 / (1.0 - omega[None, :] / omega0)
    return np.fft.ifft(Aw * inv, axis=1)


def first_order_inverse_operator(A, omega, omega0):
    """Optional first-order approximation: 1 - i/omega0 d/dt."""
    Aw = np.fft.fft(A, axis=1)
    op = (1.0 - omega[None, :] / omega0)
    return np.fft.ifft(Aw * op, axis=1)


def compute_p_nl(A, t, dt, params, ne_rt, dn_dt_rt):
    I = intensity_from_field(A, params["n0"])
    p_e = p_electronic(A, I, params["n0"], params["n2"])
    Q = q_response(I, dt, t, params["n_r"], params["n0"], 1.0, params["omega_r"], params["gamma_r"])
    p_r = params["chi_l"] * Q * A
    omega_p2 = ne_rt * E_CHARGE**2 / (M_E * EPS0)
    p_f = p_free(A, params["omega0"], omega_p2, nu_e=0.0)
    p_i = p_ion(A, dn_dt_rt, params["ip_j"], params["n0"], params["omega0"])
    p_tot = p_e + p_r + p_f + p_i

    inverse_mode = params.get("inverse_mode", "strict")
    if inverse_mode == "strict":
        return strict_inverse_operator(p_tot, params["omega"], params["omega0"])
    if inverse_mode == "first_order":
        return first_order_inverse_operator(p_tot, params["omega"], params["omega0"])
    raise ValueError(f"Unknown inverse_mode: {inverse_mode}")
