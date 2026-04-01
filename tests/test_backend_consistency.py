import numpy as np
from filament.backend import get_xp, to_device, asnumpy

def test_cpu_gpu_small_consistency_or_skip():
    np_arr = np.arange(10.0)
    cpu = asnumpy(to_device(np_arr, use_gpu=False))
    gpu_xp = get_xp(use_gpu=True)
    dev = to_device(np_arr, use_gpu=True)
    back = asnumpy(dev)
    assert np.allclose(cpu, back)
    assert gpu_xp is not None
