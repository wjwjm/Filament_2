# Filament (Stage-1 single-pulse scaffold)

## Install (CPU)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Install (GPU with CuPy)
Install CUDA-compatible CuPy package, then:
```bash
pip install -e .
```
If CuPy/GPU is unavailable, runtime falls back to NumPy.

## Run benchmarks
```bash
python scripts/run_case.py configs/isaacs2022_single_40fs.yaml
python scripts/run_case.py configs/isaacs2022_single_120fs.yaml
python scripts/plot_isaacs2022_singlepulse.py \
  outputs/isaacs2022_single_40fs/results.npz \
  outputs/isaacs2022_single_120fs/results.npz \
  --out outputs/ne_peak_vs_z.png
```

## Output
- Raw data: `outputs/<case>/results.npz`
- Plot: `outputs/ne_peak_vs_z.png`

## Implemented in stage-1
- 2D+1 (r,t,z) prototype with Gaussian beam + lens phase.
- 对称 Strang split-step：半线性(色散+轴对称衍射)+全非线性+半线性。
- 非线性项：Kerr、Raman(FFT因果卷积)、free-electron、ionization damping。
- 每个 z 步上用 RK4 更新各组分等离子体密度。
- Two ionization backends with selector: `talebpour1999` and `popruzhenko2008`.

## Not yet implemented
- Full 3D+1 (x,y,t,z) production model.
- Pulse-train thermal screens and inter-pulse fluid dynamics.
- Adaptive-z error control logic beyond interface placeholder.
