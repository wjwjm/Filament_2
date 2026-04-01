import numpy as np
from filament.propagation.nonlinear_operator import strict_inverse_operator


def test_strict_inverse_operator_finite():
    t = np.linspace(-1e-12, 1e-12, 256)
    w = 2 * np.pi * np.fft.fftfreq(t.size, d=t[1]-t[0])
    A = np.exp(-t[None, :]**2 / (100e-15)**2) + 0j
    out = strict_inverse_operator(A, w, 2.356e15)
    assert np.all(np.isfinite(out))
