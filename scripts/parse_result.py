#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) < 4:
        print("用法: python parse_result.py <final_result.txt> <candidates.tsv> <summary.txt> [evalue_threshold]")
        sys.exit(1)
    in_file = sys.argv[1]
    tsv_out = sys.argv[2]
    sum_out = sys.argv[3]
    e_cut = float(sys.argv[4]) if len(sys.argv) > 4 else 0.001

    hits = []
    with open(in_file) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) < 11:
                continue
            try:
                evalue = float(parts[10])
            except:
                continue
            if evalue < e_cut:
                hits.append(parts)

    hits.sort(key=lambda x: float(x[10]))

    with open(tsv_out, 'w') as f:
        f.write('qseqid\tsseqid\tpident\tlength\tmismatch\tgapopen\tqstart\tqend\tsstart\tsend\tevalue\tbitscore\n')
        for h in hits:
            f.write('\t'.join(h) + '\n')

    n = len(hits)
    if n == 0:
        summary = f'未发现 E-value < {e_cut} 的候选 Acr 蛋白。\n'
    else:
        best = hits[0]
        summary = f'共发现 {n} 个候选 Acr 蛋白 (E-value < {e_cut})。\n最佳候选: {best[1]} (E-value = {float(best[10]):.2e})\n详细列表见 {tsv_out}\n'
    with open(sum_out, 'w') as f:
        f.write(summary)

    print(f'✅ 已生成 {tsv_out} 和 {sum_out}')

if __name__ == '__main__':
    main()