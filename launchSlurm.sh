#!/bin/bash

#SBATCH --mail-user=cstansbu@umich.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --time=96:00:00
#SBATCH --account=indikar0
#SBATCH --partition=standard

## build the workflow from the most current snakefile
cp Snakefile workflow.smk
echo "Built Workflow..."

snakemake --profile config/slurm --cores 36 --latency-wait 90 -s workflow.smk --use-conda 