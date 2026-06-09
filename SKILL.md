---
name: anti-crispr-skill
description: 从噬菌体基因组或蛋白序列中识别候选 anti-CRISPR (Acr) 蛋白，输出结构化候选表格和中文总结。适用于皮肤相关噬菌体（痤疮丙酸杆菌、金黄色葡萄球菌等）的宿主互作研究。
version: 1.0.0
author: 董昕然
---

# Anti-CRISPR Prediction Skill

## Data Location

The data directory is set by the `ACR_DATA_DIR` environment variable. If not set, default to `~/acr_data`. All data files are in the data directory:

| File | Purpose |
|------|---------|
| `databases/known_acr.faa` | Known Acr protein database (provided by user) |
| `examples/test_phage.fna` | Example input genome |
| `results/candidates.tsv` | Filtered candidate Acr table (output) |
| `results/summary.txt` | Chinese summary report (output) |

## Prerequisites

- Linux / WSL2 / macOS
- Conda (Miniconda)
- Internet access (to install dependencies)

## Installation

Run the installer script:

```bash
bash install.sh

The script will:

Create conda environment acr_skill

Install Prodigal, DIAMOND, BLAST+, Biopython

Generate environment.yml for reproducibility

Usage
Full prediction workflow (from genome FASTA)
bash
conda activate acr_skill
python scripts/run_acr_skill.py -i your_phage.fna -o output_dir --db /path/to/known-acr.faa
Optional arguments
Argument	Description	Default
-i, --input	Input phage genome FASTA (.fna)	required
-o, --output	Output directory for results	required
--db	Known Acr protein database (.faa)	required
--evalue	E-value threshold	0.001
--threads	CPU threads	4
Example
bash
python scripts/run_acr_skill.py -i examples/test_phage.fna -o results --db known-acr.faa --evalue 0.001
Parse existing DIAMOND results (skip gene prediction and search)
If you already have a final_result.txt from DIAMOND, you can generate the TSV and summary without re-running the full pipeline:

bash
conda activate acr_skill
python scripts/parse_result.py final_result.txt candidates.tsv summary.txt 0.001
Output
File	Format	Content
candidates.tsv	TSV	12-column DIAMOND output (qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore), filtered by E-value and sorted
summary.txt	Text	Chinese summary: number of candidates, best hit (Acr name, E-value)
Example summary.txt
text
发现 3 个候选 Acr 蛋白 (E-value < 0.001)。
最佳候选: AcrIIA1 (查询蛋白 gene_123, E-value = 2.30e-10)
详细列表见 /path/to/candidates.tsv
Workflow Steps
Gene prediction (if input is .fna): prodigal -i input.fna -a tmp.faa

Build DIAMOND database from user-provided Acr DB: diamond makedb --in acr.faa -d tmp.dmnd

BLASTP search: diamond blastp -d tmp.dmnd -q tmp.faa -o final_result.txt --evalue 0.001

Filtering & parsing: Read final_result.txt, keep rows with evalue < threshold, sort by evalue, write TSV and summary.

Cleanup: Remove temporary .faa, .dmnd files.

Configuration
Edit settings.template.json to change default parameters:

json
{
    "evalue": 0.001,
    "threads": 4,
    "db_path": "/path/to/default/acr.faa"
}
Project Background
This skill is designed for skin-associated bacteriophages, especially those infecting:

Cutibacterium acnes

Staphylococcus aureus

Staphylococcus epidermidis

Klebsiella pneumoniae

Acr proteins help phages evade CRISPR-Cas immunity but are highly diverse, making homology‑based detection challenging. This workflow standardizes Acr prediction using sequence similarity with flexible filtering.

Future Extensions
Integration of PaCRISPR / AcRanker machine learning validation

Batch processing of multiple genomes

Defense system annotation (DefenseFinder, PADLOC)

AI‑assisted biological interpretation

References
AcrFinder: Yi H et al. Nucleic Acids Res (2020)

PaCRISPR: Wang J et al. Nucleic Acids Res (2020)

AcRanker: Eitzinger S et al. Genes (2020)