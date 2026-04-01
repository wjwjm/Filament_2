from __future__ import annotations
import numpy as np
from filament.constants import EPS0, C

def intensity_from_field(A, n0=1.0):
    return 0.5 * n0 * EPS0 * C * np.abs(A)**2
