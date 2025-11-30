#!/bin/bash
# --- 1. Richiesta Risorse (MODIFICATA PER ARRAY) ---
#PBS -N clusterings_Array # Nuovo nome per l'array

# 1. DEFINIZIONE DEL JOB ARRAY: Crea 25 job separati (0 a 24)
#    Ogni job eseguirà un'unica iterazione del tuo esperimento.
#PBS -t 0-24%8

# Risorse per OGNI SINGOLO JOB nell'array:
# Un nodo, 4 core. (Adattato da 8ppn a 4ppn, più comune per i nodi, ma puoi lasciare 8 se preferisci)
#PBS -l nodes=1:ppn=4 

# WALLTIME RIDOTTO: Tempo stimato per UN SOLO esperimento (es. 45 minuti).
# Non è più il tempo totale, ma il tempo massimo per la singola run più lunga.
#PBS -l walltime=00:45:00 
# Memoria per UN SINGOLO esperimento (mantenuta alta per sicurezza)
#PBS -l mem=32gb 


# --- 2. Caricamento Moduli Software ---
module load env/software/doduo

module load Python/3.11.5-GCCcore-13.2.0



source $VSC_DATA/venv/bin/activate



# Variabile d'ambiente per il parallelismo interno di NumPy/Scikit-learn
export OMP_NUM_THREADS=4 # Deve corrispondere al valore di ppn (4)


# --- 3. Setup e Esecuzione (MODIFICATA) ---
# Vai alla directory di submission
cd $PBS_O_WORKDIR


# Copia i dati e lo script nella directory temporanea veloce
# Nota: i nomi dei file di input sono stati corretti per la lettura diretta
cp $PBS_O_WORKDIR/datasets/human_blood_mass_cytometry_batch1.csv $TMPDIR/

cp $PBS_O_WORKDIR/datasets/human_blood_mass_cytometry_batch1_metadata.csv $TMPDIR/

cp $PBS_O_WORKDIR/agglomerative.py $TMPDIR/ # USA IL NUOVO NOME DELLO SCRIPT


# Vai alla directory temporanea per eseguire lo script
cd $TMPDIR


TASK_ID=$PBS_ARRAYID 

# Verifica che la variabile sia popolata (questa riga è solo un controllo)
echo "L'indice del task corrente è: $TASK_ID" 

# 2. Esegui lo script Python, usando la variabile locale $TASK_ID
python agglomerative.py $TASK_ID
echo "step 8: Esecuzione Python terminata"


# --- 4. Copia Risultati (USA LA NUOVA VARIABILE TASK_ID) ---
cp agglomerative_results_${TASK_ID}.csv $VSC_HOME/agglomerative_array_results_${TASK_ID}.csv
echo "step 9: Risultati copiati"


