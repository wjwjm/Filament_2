from __future__ import annotations
import numpy as np
from filament.diagnostics.intensity import intensity_from_field
from filament.diagnostics.electron_density import ne_peak
from filament.propagation.linear_operator import apply_linear_half_step
from filament.propagation.nonlinear_operator import compute_p_nl
from filament.plasma.plasma_update import update_species_density_rk4


def solve_single_pulse_rt(grid, A0, species_list, rate_funcs, params, z_stepper):
    """2D+1 (r,t,z) axisymmetric single-pulse solver (Strang split)."""
    A = A0.copy()
    ne_curves, z_cm = [], []
    nj = [np.zeros_like(A.real) for _ in species_list]

    params = dict(params)
    params["omega"] = grid.omega

    for iz, z in enumerate(grid.z):
        dz = z_stepper.next_dz()

        # half linear step
        if iz > 0:
            A = apply_linear_half_step(A, grid.omega, grid.r, grid.dr, dz, params["k0"], params["beta2"])

        # plasma update + nonlinear full step
        I = intensity_from_field(A, params["n0"])
        dn_dt_sum = np.zeros_like(I)
        ne = np.zeros_like(I)
        for j, sp in enumerate(species_list):
            nj[j] = update_species_density_rk4(nj[j], sp.density_m3, grid.dt, rate_funcs[j], I)
            dn = rate_funcs[j](I) * (sp.density_m3 - nj[j])
            dn_dt_sum += dn
            ne += nj[j]

        p_nl = compute_p_nl(A, grid.t, grid.dt, params, ne, dn_dt_sum)
        A = A + 1j * dz * p_nl

        # half linear step
        A = apply_linear_half_step(A, grid.omega, grid.r, grid.dr, dz, params["k0"], params["beta2"])

        ne_curves.append(ne_peak(ne))
        z_cm.append((z - params["vacuum_focus_m"]) * 100.0)

    return np.array(z_cm), np.array(ne_curves), A
