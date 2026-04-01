from filament.units import cm_to_m, fs_to_s, ev_to_j

def test_units_basic():
    assert cm_to_m(1.0) == 1e-2
    assert fs_to_s(1.0) == 1e-15
    assert abs(ev_to_j(1.0) - 1.602176634e-19) < 1e-30
