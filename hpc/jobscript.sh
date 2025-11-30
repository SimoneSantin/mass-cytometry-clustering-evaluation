#!/bin/bash
# --- 1. Richiesta Risorse (PBS Commands) ---
#PBS -N kmeans_prova # Nome del job
#PBS -l nodes=1:ppn=8
#PBS -l walltime=6:30:00 
#PBS -l mem=64gb

# --- 2. Caricamento Moduli Software ---
module load env/software/doduo

module load Python/3.11.5-GCCcore-13.2.0

source $VSC_DATA/venv/bin/activate

# --- 3. Setup e Esecuzione ---
# Vai alla directory di submission
cd $PBS_O_WORKDIR

# Copia i dati e lo script nella directory temporanea veloce
cp $PBS_O_WORKDIR/datasets/human_blood_mass_cytometry_batch1.csv $TMPDIR
cp $PBS_O_WORKDIR/datasets/human_blood_mass_cytometry_batch1_metadata.csv $TMPDIR
cp $PBS_O_WORKDIR/prova.py $TMPDIR

# Vai alla directory temporanea per eseguire lo script
cd $TMPDIR

# Esegui lo script Python
python prova.py
