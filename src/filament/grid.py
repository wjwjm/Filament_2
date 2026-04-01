from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class RTGrid:
    nr: int
    nt: int
    nz: int
    r_max_m: float
    t_max_s: float
    z_max_m: float

    def __post_init__(self):
        self.r = np.linspace(0.0, self.r_max_m, self.nr)
        self.t = np.linspace(-self.t_max_s, self.t_max_s, self.nt)
        self.dr = self.r[1] - self.r[0]
        self.dt = self.t[1] - self.t[0]
        self.z = np.linspace(0.0, self.z_max_m, self.nz)
        self.dz = self.z[1] - self.z[0] if self.nz > 1 else self.z_max_m
        self.omega = 2 * np.pi * np.fft.fftfreq(self.nt, d=self.dt)

    def sampling_warnings(self):
        warns = []
        if self.nt < 256:
            warns.append("nt < 256 may under-resolve Raman convolution")
        if self.nr < 64:
            warns.append("nr < 64 may under-resolve filament core")
        return warns
