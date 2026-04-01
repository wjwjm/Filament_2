from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Species:
    name: str
    fraction: float
    density_m3: float
    ip_ev: float
    z_eff: float
    n_star: float
