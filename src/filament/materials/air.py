from __future__ import annotations
from .species import Species

AIR_DENSITY_M3 = 2.5e25
N2 = Species("N2", 0.8, AIR_DENSITY_M3 * 0.8, 15.576, 0.9, 1.0)
O2 = Species("O2", 0.2, AIR_DENSITY_M3 * 0.2, 12.55, 0.53, 1.0)

# Isaacs 2022 single-pulse settings at 800 nm
N2_KERR_M2_W = 0.78e-23  # 0.78e-19 cm^2/W
BETA2_S2_M = 0.20e-30 / 1e-2  # 0.20 fs^2/cm
RAMAN_N2_M2_W = 2.3e-23  # 2.3e-19 cm^2/W
OMEGA_R = 1.6e13
GAMMA_R = 1.3e13
N0 = 1.0003
