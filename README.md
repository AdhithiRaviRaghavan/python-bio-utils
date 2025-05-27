# python-bio-utils

A collection of Python scripts for bioinformatics tasks, developed for coursework and personal exploration.  
These tools demonstrate practical use of file parsing, sequence analysis, and command-line scripting with a focus on biological data formats like FASTA, GFF, and SAM.

---

## 📁 Contents

| Script                      | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `seq_tools.py`             | Utilities to load FASTA files, compute reverse complements, find ORFs, and translate DNA to protein. |
| `SAMParser.py`             | Extracts transcript-level read counts from aligned SAM/BAM files.           |
| `homology.py`              | Identifies reciprocal best homologs based on pairwise BLAST XML comparisons.|
| `gene_annotation_search.py`| CLI tool to search an SQLite gene annotation database by keyword.           |
| `gffparser.py`             | Extracts gene names from GFF files by chromosome and coordinate range.      |
| `test.py`, `test_debug.py` | Miscellaneous or scratch code for testing ideas.                            |

---

## 🧪 Features

- Manual parsing of GFF, FASTA, and BLAST formats
- Command-line interfaces using `argparse`
- Clean class-based sequence utilities
- Spike-in normalization and data extraction workflows

---

## 🚀 Getting Started

Each script is standalone. You can run any tool from the command line. Example:

```bash
python gffparser.py -i example.gff -c Chr1 -s 10000 -e 50000
