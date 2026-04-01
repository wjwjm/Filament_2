import numpy as np
from filament.plasma.plasma_update import update_species_density_rk4

def test_rk4_clamped():
    I = np.ones((2,3))*1e16
    nj = np.zeros_like(I)
    nj0 = 1e20
    rate = lambda x: np.ones_like(x)*1e14
    out = update_species_density_rk4(nj, nj0, 1e-15, rate, I)
    assert np.all(out <= nj0)
    assert np.all(out >= 0)
