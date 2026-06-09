#!/usr/bin/env python3
import subprocess
import argparse
import os

def main():
    p = argparse.ArgumentParser(description='Anti-CRISPR 识别流程')
    p.add_argument('-i', '--input', required=True, help='输入 .fna 文件')
    p.add_argument('-o', '--output', required=True, help='输出目录')
    p.add_argument('--db', required=True, help='已知 Acr 蛋白数据库 (.faa)')
    p.add_argument('--evalue', type=float, default=0.001, help='E-value 阈值')
    p.add_argument('--threads', type=int, default=4, help='线程数')
    args = p.parse_args()

    os.makedirs(args.output, exist_ok=True)
    tmp_faa = os.path.join(args.output, 'tmp_genes.faa')
    tmp_dmnd = os.path.join(args.output, 'tmp_acr.dmnd')
    raw_out = os.path.join(args.output, 'final_result.txt')

    # 1. 基因预测
    subprocess.run(f'prodigal -i {args.input} -a {tmp_faa} -q', shell=True, check=True)
    # 2. 构建 DIAMOND 数据库
    subprocess.run(f'diamond makedb --in {args.db} -d {tmp_dmnd}', shell=True, check=True)
    # 3. 比对
    subprocess.run(f'diamond blastp -d {tmp_dmnd} -q {tmp_faa} -o {raw_out} --evalue {args.evalue} --threads {args.threads}', shell=True, check=True)
    # 4. 解析结果
    parse_script = os.path.join(os.path.dirname(__file__), 'parse_result.py')
    tsv_out = os.path.join(args.output, 'candidates.tsv')
    sum_out = os.path.join(args.output, 'summary.txt')
    subprocess.run(f'python {parse_script} {raw_out} {tsv_out} {sum_out} {args.evalue}', shell=True, check=True)
    # 5. 清理临时文件
    for f in [tmp_faa, tmp_dmnd]:
        if os.path.exists(f):
            os.remove(f)
    print(f'✅ 完成！结果保存在 {tsv_out} 和 {sum_out}')

if __name__ == '__main__':
    main()