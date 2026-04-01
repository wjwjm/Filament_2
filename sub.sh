#!/bin/bash
#SBATCH -J filament
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH -t 02:00:00

set -euo pipefail

# 进入提交目录（Slurm 推荐），兜底到脚本目录
cd "${SLURM_SUBMIT_DIR:-$(cd "$(dirname "$0")" && pwd)}"

# 可覆盖参数：CFG
CFG="${CFG:-configs/isaacs2022_single_120fs.yaml}"

if [[ ! -f "$CFG" ]]; then
  echo "[fatal] 配置文件不存在: $CFG"
  exit 3
fi

# 线程数与 Slurm 对齐
if [[ -n "${SLURM_CPUS_PER_TASK:-}" ]]; then
  export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
  export OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
  export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
  export NUMEXPR_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
fi

# 可选：根据集群环境启用 conda（不存在则跳过）
if command -v conda >/dev/null 2>&1; then
  source "$(conda info --base)/etc/profile.d/conda.sh" || true
  if conda env list | awk '{print $1}' | grep -qx "Filament_python"; then
    conda activate Filament_python
  fi
fi

export PYTHONUNBUFFERED=1

echo "[info] 使用配置: $CFG"
echo "[info] 输出目录由配置文件中的 output.dir 决定"
echo "[info] 提交命令示例: sbatch --gpus=1 ./sub.sh"

python scripts/run_case.py "$CFG"

echo "[done] 运行完成。"
