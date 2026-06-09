#!/bin/bash
set -e

echo "=== Anti-CRISPR Skill 安装脚本 ==="

if ! command -v conda &> /dev/null; then
    echo "错误: 未找到 conda，请先安装 Miniconda。"
    exit 1
fi

if conda env list | grep -q "acr_skill"; then
    echo "环境 acr_skill 已存在，跳过创建。"
else
    echo "创建 conda 环境 acr_skill ..."
    conda create -n acr_skill python=3.9 -y
fi

echo "安装依赖工具 (prodigal, diamond, blast)..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate acr_skill
conda install -c bioconda prodigal diamond blast -y
conda install -c conda-forge biopython -y

echo "安装完成！"
echo "激活环境: conda activate acr_skill"
echo "运行示例: python scripts/run_acr_skill.py -i input.fna -o output --db /path/to/acr.faa"