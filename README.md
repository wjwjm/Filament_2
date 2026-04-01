# Filament（阶段 1：单脉冲脚手架）

本项目实现了一个用于超短激光丝化传播的 **2D+1（r,t,z）轴对称原型求解器**，用于复现实验文献中的单脉冲基准算例，并为后续 3D+1 与脉冲串扩展打基础。

## 1. 安装

### 1.1 CPU 环境
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 1.2 GPU 环境（CuPy）
先安装与你 CUDA 版本匹配的 CuPy，再安装本项目：
```bash
pip install -e .
```
若 CuPy 或 GPU 不可用，程序会自动回退到 NumPy。

## 2. 运行基准案例

```bash
python scripts/run_case.py configs/isaacs2022_single_40fs.yaml
python scripts/run_case.py configs/isaacs2022_single_120fs.yaml
python scripts/plot_isaacs2022_singlepulse.py \
  outputs/isaacs2022_single_40fs/results.npz \
  outputs/isaacs2022_single_120fs/results.npz \
  --out outputs/ne_peak_vs_z.png
```

## 3. 在超算上提交（Slurm）

仓库根目录已提供与本项目匹配的 `sub.sh`。

推荐提交方式（你指定的命令）：
```bash
sbatch --gpus=1 ./sub.sh
```

可选覆盖参数示例：
```bash
sbatch --gpus=1 --export=ALL,CFG=configs/isaacs2022_single_40fs.yaml ./sub.sh
```

## 4. 输出文件

- 原始数据：`outputs/<case>/results.npz`
- 配置快照：`outputs/<case>/config_snapshot.json`
- 对比图（可选）：`outputs/ne_peak_vs_z.png`

## 5. 阶段 1 已实现功能

- 2D+1（r,t,z）原型：高斯光束 + 薄透镜相位。
- 对称 Strang split-step：半线性（色散 + 轴对称衍射）+ 全非线性 + 半线性。
- 非线性项：Kerr、Raman（FFT 因果卷积）、free-electron、ionization damping。
- 每个 z 步用 RK4 更新多组分等离子体密度。
- 双电离后端可选：`talebpour1999` 与 `popruzhenko2008`。

## 6. 暂未实现

- 完整 3D+1（x,y,t,z）生产级模型。
- 脉冲串热屏与脉间流体动力学。
- 超出当前接口占位符的自适应 z 步长误差控制。

## 7. 文献与资料

所有 PDF 参考文献已统一整理至：

- `references/pdfs/`

映射说明见：

- `docs_mapping.md`
- `references/README.md`
