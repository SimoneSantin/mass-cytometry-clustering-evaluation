import sys
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, adjusted_rand_score, normalized_mutual_info_score
import time

sample_sizes = [10000, 20000, 40000, 60000, 80000]
n_runs = 5
total_jobs = len(sample_sizes) * n_runs

if len(sys.argv) < 2:
    print("Error missing argument(sys.argv[1]).")
    sys.exit(1)

try:
    JOB_INDEX = int(sys.argv[1]) 
    if not (0 <= JOB_INDEX < total_jobs):
        raise ValueError
except (ValueError, IndexError):
    print(f"Error job index not valid ({sys.argv[1]})")
    sys.exit(1)

size_index = JOB_INDEX // n_runs 
run_index = JOB_INDEX % n_runs   

size = sample_sizes[size_index]
run = run_index

try:
    data_markers = pd.read_csv("human_blood_mass_cytometry_batch1.csv", index_col=0)
    data_celltypes = pd.read_csv("human_blood_mass_cytometry_batch1_metadata.csv") 
except FileNotFoundError as e:
    print(f"ERROR dataset not found")
    sys.exit(1)

labels_true = data_celltypes["cell_type"].values

results = [] 


np.random.seed(100 + run)
start = np.random.randint(0, len(data_markers) - size + 1)
X = data_markers.iloc[start:start+size]
Y = labels_true[start:start+size]
print(f"Job {JOB_INDEX} (Size: {size}, Run: {run}),first index selected: {start}")


start_time = time.time()
try:
   
    db = DBSCAN(
        eps=2.5,
        min_samples=5,
        metric='euclidean'
            )
    labels = db.fit_predict(X)

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


df = pd.DataFrame(results)

df.to_csv(f"dbscan_results_{JOB_INDEX}.csv", index=False)

print(f"\nSaved results for Job {JOB_INDEX} to dbscan_results_{JOB_INDEX}.csv")