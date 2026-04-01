from __future__ import annotations
from .constants import CM, FS, EV

def cm_to_m(x): return x * CM
def m_to_cm(x): return x / CM
def fs_to_s(x): return x * FS
def s_to_fs(x): return x / FS
def ev_to_j(x): return x * EV
def j_to_ev(x): return x / EV
