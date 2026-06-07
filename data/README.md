# Data Notes

This directory contains the current AMR-Bench-mini pilot data.

## Files

- `metadata.json`: BV-BRC isolate metadata for 60 *Klebsiella pneumoniae*
  isolates.
- `ast.json`: laboratory AST records from BV-BRC.
- `fasta/`: local genome assembly FASTA files.
- `card/`: CARD snapshot files.
- `tasks/`: generated benchmark tasks.

## AST Handling

The task builder preserves source AST fields including:

- phenotype label
- measurement
- measurement unit
- measurement sign
- laboratory method
- testing standard
- testing standard year, if present

When duplicate AST records exist for the same isolate and antibiotic, the builder
keeps all source records in the task and uses the first label only when all
available labels agree.

## Clinical Boundary

These retrospective AST labels are benchmark labels, not treatment
recommendations. The generated tasks should not be used for clinical decision
support.
