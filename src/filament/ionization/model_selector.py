from __future__ import annotations
from filament.ionization.talebpour1999 import rate_talebpour
from filament.ionization.popruzhenko2008 import rate_popruzhenko, PopruzhenkoSpeciesParams


def build_rate_function(model_name: str, omega0: float, species):
    if model_name == "talebpour1999":
        return lambda I: rate_talebpour(I, species, omega0)
    if model_name == "popruzhenko2008":
        p = PopruzhenkoSpeciesParams(ip_ev=species.ip_ev, Z=species.z_eff, n_star=species.n_star)
        return lambda I: rate_popruzhenko(I, p, omega0)
    raise ValueError(f"Unknown ionization model: {model_name}")
