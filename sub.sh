#!/bin/bash
#SBATCH -J filament_single
#SBATCH -p cpu
#SBATCH -N 1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH -t 02:00:00
#SBATCH -o logs/%x-%j.out
#SBATCH -e logs/%x-%j.err

set -euo pipefail

# 用法：sbatch sub.sh [40|120|both]
CASE="${1:-both}"

mkdir -p logs outputs

# 根据集群环境自行替换：module/anaconda/venv
if [ -f "${HOME}/.bashrc" ]; then
  source "${HOME}/.bashrc"
fi

# 示例：激活你的 Python 环境
# source ~/miniconda3/bin/activate filament
# 或
# source .venv/bin/activate

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}

run_case() {
  local cfg=$1
  echo "[INFO] running ${cfg}"
  python scripts/run_case.py "${cfg}"
}

if [ "${CASE}" = "40" ]; then
  run_case configs/isaacs2022_single_40fs.yaml
elif [ "${CASE}" = "120" ]; then
  run_case configs/isaacs2022_single_120fs.yaml
else
  run_case configs/isaacs2022_single_40fs.yaml
  run_case configs/isaacs2022_single_120fs.yaml
  python scripts/plot_isaacs2022_singlepulse.py \
    outputs/isaacs2022_single_40fs/results.npz \
    outputs/isaacs2022_single_120fs/results.npz \
    --out outputs/ne_peak_vs_z.png
fi

echo "[INFO] done"
