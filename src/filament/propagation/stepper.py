from __future__ import annotations
from dataclasses import dataclass

@dataclass
class FixedStepZ:
    dz: float
    def next_dz(self, _state=None):
        return self.dz

@dataclass
class AdaptiveStepZ:
    dz_init: float
    tol: float
    def next_dz(self, _state=None):
        return self.dz_init
