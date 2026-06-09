# Anti-CRISPR Prediction Skill

A skill for identifying candidate anti-CRISPR (Acr) proteins from phage genome sequences, with automated filtering and Chinese summary reports.

## Features

- **One-shot prediction**: Input a phage genome (.fna) → get candidates.tsv and summary.txt in one command
- **Automated pipeline**: Gene prediction (Prodigal) → Homology search (DIAMOND) → E-value filtering → Report generation
- **Flexible thresholds**: Customize E-value cutoff and CPU threads
- **Clean output**: Structured TSV table + human-readable Chinese summary
- **Minimal dependencies**: Conda environment with Prodigal, DIAMOND, BLAST+, Biopython

## Quick Start

### 1. Install

Clone this repo and run the installer:

```bash
git clone 
cd anti-crispr-skill
bash install.sh
The installer will:

Create conda environment acr_skill (Python 3.9)

Install Prodigal, DIAMOND, BLAST+, Biopython

Export environment.yml for reproducibility

2. Prepare an Acr database
You need a known Acr protein database (.faa). Download it with:

bash
wget -O known-acr.faa https://raw.githubusercontent.com/HaidYi/acrfinder/master/dependencies/diamond_query/known-acr.faa
3. Run prediction
bash
conda activate acr_skill
python scripts/run_acr_skill.py -i your_phage.fna -o output_dir --db /path/to/known-acr.faa
Usage
Command	What it does
-i, --input	Input phage genome FASTA (.fna)
-o, --output	Output directory for results
--db	Known Acr protein database (.faa)
--evalue	E-value threshold (default: 0.001)
--threads	CPU threads (default: 4)
Example
bash
python scripts/run_acr_skill.py -i examples/test_phage.fna -o results --db known-acr.faa --evalue 0.001
Output
File	Format	Content
candidates.tsv	TSV	12-column DIAMOND output (qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore), filtered and sorted by E-value
summary.txt	Text	Chinese summary: number of candidates, best hit (Acr name, E-value)
Example summary.txt
text
发现 3 个候选 Acr 蛋白 (E-value < 0.001)。
最佳候选: AcrIIA1 (查询蛋白 gene_123, E-value = 2.30e-10)
详细列表见 /path/to/candidates.tsv
Requirements
Linux / WSL2 / macOS

Conda (Miniconda)

Internet access (to download dependencies and database)

File Structure
text
anti-crispr-skill/
├── SKILL.md                  # Claude Code skill definition
├── README.md                 # This file
├── install.sh                # One-step installer
├── settings.template.json    # Default settings (evalue, threads, db_path)
├── .gitignore                # Git ignore rules
└── scripts/
    ├── run_acr_skill.py      # Main prediction workflow
    └── parse_result.py       # Result parser (filtering + summary)
Configuration
Edit settings.template.json to change defaults:

json
{
    "evalue": 0.001,
    "threads": 4,
    "db_path": "/path/to/default/acr.faa"
}
License
MIT

References
AcrFinder: Yi H et al. Nucleic Acids Res (2020)

Prodigal: Hyatt D et al. BMC Bioinformatics (2010)

DIAMOND: Buchfink B et al. Nat Methods (2021)