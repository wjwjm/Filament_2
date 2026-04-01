from __future__ import annotations
import argparse, os, json
import numpy as np
from filament.constants import C
from filament.units import fs_to_s
from filament.grid import RTGrid
from filament.pulse import gaussian_pulse_rt
from filament.lens import thin_lens_phase
from filament.materials.air import N2, O2, N2_KERR_M2_W, BETA2_S2_M, RAMAN_N2_M2_W, OMEGA_R, GAMMA_R, N0
from filament.ionization.model_selector import build_rate_function
from filament.propagation.stepper import FixedStepZ
from filament.propagation.nee_solver import solve_single_pulse_rt
from filament.utils.io import load_config, save_npz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    args = ap.parse_args()
    cfg = load_config(args.config)

    lam = cfg["lambda0_nm"] * 1e-9
    omega0 = 2*np.pi*C/lam
    k0 = 2*np.pi/lam
    f = cfg["f_m"]
    w0 = f / cfg["f_number"] / 2.0

    g = cfg["grid"]
    grid = RTGrid(g["nr"], g["nt"], g["nz"], g["r_max_mm"]*1e-3, fs_to_s(g["t_max_fs"]), g["z_max_m"])

    A0 = gaussian_pulse_rt(grid.r, grid.t, cfg["p_peak_w"], fs_to_s(cfg["tau_fwhm_fs"]), w0, n0=N0)
    A0 *= thin_lens_phase(grid.r, k0, f)

    species = [N2, O2]
    rate_funcs = [build_rate_function(cfg["ionization"]["model"], omega0, sp) for sp in species]
    params = {
        "omega0": omega0,
        "k0": k0,
        "beta2": BETA2_S2_M,
        "n2": N2_KERR_M2_W,
        "n_r": RAMAN_N2_M2_W,
        "omega_r": OMEGA_R,
        "gamma_r": GAMMA_R,
        "chi_l": 1.0,
        "n0": N0,
        "ip_j": N2.ip_ev * 1.602176634e-19,
        "vacuum_focus_m": f,
        "inverse_mode": "strict",
    }
    z, nepk, _ = solve_single_pulse_rt(grid, A0, species, rate_funcs, params, FixedStepZ(grid.dz))

    outdir = cfg["output"]["dir"]
    os.makedirs(outdir, exist_ok=True)
    save_npz(f"{outdir}/results.npz", z_from_focus_cm=z, ne_peak_m3=nepk)
    with open(f"{outdir}/config_snapshot.json", "w", encoding="utf-8") as fcfg:
        json.dump(cfg, fcfg, indent=2, ensure_ascii=False)
    print(f"Saved {outdir}/results.npz")

if __name__ == "__main__":
    main()
