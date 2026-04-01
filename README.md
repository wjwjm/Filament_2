# 超短脉冲成丝模拟（阶段一：单脉冲）

本项目用于搭建可扩展到高重频脉冲列的科研代码框架。当前阶段仅实现 **单脉冲** 在空气中的传播原型（2D+1 轴对称 `r,t,z`），目标诊断量为 `ne_peak(z)`。

## 1. 项目现状

- 已实现：
  - 对称 Strang 分步推进（线性半步 + 非线性全步 + 线性半步）
  - 线性色散（`beta2`）与轴对称衍射
  - Kerr、Raman（因果卷积）、自由电子项与电离阻尼项
  - 等离子体组分密度 RK4 更新
  - 两套可切换电离后端：`talebpour1999` / `popruzhenko2008`
- 未实现（留待下一阶段）：
  - 高重频脉冲列热屏、脉冲间流体演化
  - 全 3D+1 (`x,y,t,z`) 版本

## 2. 安装

### 2.1 CPU 环境

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 2.2 GPU 环境（CuPy）

先安装与你 CUDA 对应的 CuPy，再安装本项目：

```bash
pip install -e .
```

> 若 CuPy/GPU 不可用，代码会自动回退到 NumPy。

## 3. 运行基准工况

```bash
python scripts/run_case.py configs/isaacs2022_single_40fs.yaml
python scripts/run_case.py configs/isaacs2022_single_120fs.yaml
python scripts/plot_isaacs2022_singlepulse.py \
  outputs/isaacs2022_single_40fs/results.npz \
  outputs/isaacs2022_single_120fs/results.npz \
  --out outputs/ne_peak_vs_z.png
```

## 4. 输出内容

- 原始数据：`outputs/<case>/results.npz`
- 配置快照：`outputs/<case>/config_snapshot.json`
- 对比图：`outputs/ne_peak_vs_z.png`

## 5. 参考文献

PDF 已统一放入 `references/` 目录，见 `references/README.md`。

## 6. 目录导览

每个子目录均配有 README 文档说明其用途（见 `configs/README.md`、`scripts/README.md`、`src/**/README.md`、`tests/README.md` 等）。
