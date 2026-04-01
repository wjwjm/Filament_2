import numpy as np
from filament.ionization.talebpour1999 import rate_talebpour
from filament.ionization.popruzhenko2008 import rate_popruzhenko, PopruzhenkoSpeciesParams
from filament.materials.air import N2

def test_talebpour_monotonic():
    I = np.logspace(13, 15, 8) * 1e4
    r = rate_talebpour(I, N2, 2.356e15)
    assert np.all(np.diff(r) >= 0)

def test_pop_no_nan_inf():
    I = np.logspace(12, 15, 16) * 1e4
    p = PopruzhenkoSpeciesParams(ip_ev=15.576, Z=1.0, n_star=1.0)
    r = rate_popruzhenko(I, p, 2.356e15)
    assert np.all(np.isfinite(r))
