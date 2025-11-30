import sys
import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, adjusted_rand_score, normalized_mutual_info_score
import time

# --- 1. Definizione delle Sequenze e Calcolo dell'Indice ---
sample_sizes = [10000, 20000, 40000, 60000, 80000]
n_runs = 5
total_jobs = len(sample_sizes) * n_runs

# Controlla che l'indice del job sia stato passato da Bash
if len(sys.argv) < 2:
    print("Errore: Manca l'indice del Job Array come argomento (sys.argv[1]).")
    sys.exit(1)

try:
    # L'indice del job (da 0 a 24) viene letto dall'argomento di sistema
    JOB_INDEX = int(sys.argv[1]) 
    if not (0 <= JOB_INDEX < total_jobs):
        raise ValueError
except (ValueError, IndexError):
    print(f"Errore: Indice del job non valido ({sys.argv[1]}). Deve essere tra 0 e {total_jobs-1}.")
    sys.exit(1)

# Mappatura dell'Indice: calcola l'indice della dimensione e l'indice della run
size_index = JOB_INDEX // n_runs  # 0, 0, 0, 0, 0, 1, 1, ...
run_index = JOB_INDEX % n_runs    # 0, 1, 2, 3, 4, 0, 1, ...

size = sample_sizes[size_index]
run = run_index

# --- 2. Caricamento Dati (Corretto) ---
# Adesso i file vengono cercati nella directory corrente ($TMPDIR)
try:
    data_markers = pd.read_csv("human_blood_mass_cytometry_batch1.csv", index_col=0)
    data_celltypes = pd.read_csv("human_blood_mass_cytometry_batch1_metadata.csv") 
except FileNotFoundError as e:
    print(f"ERRORE: Impossibile trovare i file di input in {e.filename}. Assicurati siano stati copiati correttamente in $TMPDIR.")
    sys.exit(1)

labels_true = data_celltypes["cell_type"].values

# --- 3. Esecuzione del Singolo Esperimento ---

# (Rimuovi l'inizializzazione KMeans e la valutazione singola che erano nel codice originale)
results = [] # Inizializza la lista per questa singola run

# Imposta il seme e seleziona il campione per questa specifica run
np.random.seed(100 + run)
start = np.random.randint(0, len(data_markers) - size + 1)
X = data_markers.iloc[start:start+size]
Y = labels_true[start:start+size]
print(f"Job {JOB_INDEX} (Size: {size}, Run: {run}), primo indice selezionato: {start}")


start_time = time.time()
try:
   
    # 3) Clustering con i migliori parametri
    agg = AgglomerativeClustering(
        n_clusters=best_k,
        linkage=best_link,
        metric=best_metric if best_link != "ward" else "euclidean"
    )
    labels = agg.fit_predict(X)

    # 4) Calcolo ARI e NMI
    ari = adjusted_rand_score(Y, labels)
    nmi = normalized_mutual_info_score(Y, labels)
    sil = silhouette_score(X, labels)
 


    exec_time = time.time() - start_time

    results.append({
        "sample_size": size,
        "run": run,
        "ari": ari,
        "nmi": nmi,
        "silhouette": sil,
        "num_clusters": len(np.unique(labels)),
        "time_sec": exec_time
    })

    print(f"[kmeans] Job {JOB_INDEX} | Size={size} run={run} | "
          f"ARI={ari:.4f} | NMI={nmi:.4f} | Sil={sil:.4f} | time={exec_time:.2f}s")

except Exception as e:
    print(f"FAILED: Job {JOB_INDEX}, error={e}")
    results.append({
        "sample_size": size,
        "run": run,
        "ari": np.nan, "nmi": np.nan, "silhouette": np.nan,
        "num_clusters": np.nan, "time_sec": np.nan, "error": str(e)
    })

# --- 4. Salvataggio del Risultato Unico ---
df = pd.DataFrame(results)
# SALVA con l'indice del job per evitare sovrascritture in parallelo
df.to_csv(f"agglomerative_results_{JOB_INDEX}.csv", index=False)

print(f"\nSaved results for Job {JOB_INDEX} to agglomerative_results_{JOB_INDEX}.csv")