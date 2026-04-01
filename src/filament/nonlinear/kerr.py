from __future__ import annotations
import numpy as np

def p_electronic(A, intensity, n0, n2):
    return (n0 / (2*np.pi)) * n2 * intensity * A
