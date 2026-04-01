from __future__ import annotations
import json, yaml, numpy as np
from pathlib import Path

def load_config(path):
    p = Path(path)
    if p.suffix in {'.yaml', '.yml'}:
        return yaml.safe_load(p.read_text())
    return json.loads(p.read_text())

def save_npz(path, **arrays):
    np.savez(path, **arrays)
