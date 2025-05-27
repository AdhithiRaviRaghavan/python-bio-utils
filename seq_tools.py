"""
seq_tools_.py — DNA Sequence Utility Functions

Author: Adhithi R. Raghavan
Date: May 2023

Description:
This module includes:
- fasta_load: Loads sequences from a FASTA file
- Sequence class: For reverse complement, longest ORF detection, and protein translation


Usage:
>>> seqs = fasta_load("example.fasta")
>>> s = Sequence(seqs[0])
>>> s.reverse()
>>> s.get_long()
>>> s.convert()
>>> print(s.get_orf())
"""

import re

def fasta_load(filename):
    """Load sequences from a FASTA file."""
    sequences = []
    seq = ''
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if seq:
                    sequences.append(seq)
                    seq = ''
            else:
                seq += line
        if seq:
            sequences.append(seq)
    return sequences


class Sequence:
    """DNA sequence utility class for ORF finding and translation."""

    def __init__(self, sequence):
        self.sequence = sequence.upper()
        self.converted = None
        self.genetic_code = {
            'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
            'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
            'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
            'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
            'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
            'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
            'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
            'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
            'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
            'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
            'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
            'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
            'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
            'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
            'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
            'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'
        }

    def reverse(self):
        """Return the reverse complement of the sequence."""
        complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
        reverse_complement = ''.join(complement.get(base, base) for base in reversed(self.sequence))
        return reverse_complement

    def get_long(self):
        """Find the longest ORF on both strands."""
        pattern = re.compile(r'ATG(?:...)*?(?:TAA|TAG|TGA)')
        strands = [self.sequence, self.reverse()]
        orfs = [match.group() for strand in strands for match in pattern.finditer(strand)]
        self.longest_orf = max(orfs, key=len, default='')
        return self.longest_orf

    def convert(self):
        """Translate the longest ORF into a protein sequence."""
        if not hasattr(self, 'longest_orf'):
            self.get_long()
        codons = [self.longest_orf[i:i+3] for i in range(0, len(self.longest_orf)-2, 3)]
        self.converted = ''.join(self.genetic_code.get(codon, 'X') for codon in codons)
        return self.converted

    def get_orf(self):
        """Return translated ORF (protein sequence)."""
        return self.converted if self.converted else ''
