import pandas as pd
import flowsom as fs
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, SpectralClustering, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt
import seaborn as sns
import time

# --- 1. Caricamento Dati e Campionamento ---
data_markers = pd.read_csv("human_blood_mass_cytometry_batch1.csv", index_col=0)      
data_celltypes = pd.read_csv("human_blood_mass_cytometry_batch1_metadata.csv")  
labels_true = data_celltypes["cell_type"].values

# --------------------------------------
SAMPLE_SIZE = 40000
np.random.seed(42) # Set seed per replicabilità
start = np.random.randint(0, len(data_markers) - SAMPLE_SIZE + 1)
X_sample = data_markers.iloc[start:start+SAMPLE_SIZE]
labels_true_sample = labels_true[start:start+SAMPLE_SIZE]

k_values = [2, 3, 4, 5, 6, 8, 10]
linkages = ['ward', 'average', 'complete']
metrics = {
    'ward': ['euclidean'],  
    'average': ['euclidean', 'manhattan', 'cosine'],
    'complete': ['euclidean', 'manhattan', 'cosine']
}

best_result = {
    "score": -1,
    "params": None
}

print(f"Testing parameters on sample size: {SAMPLE_SIZE} (start index: {start})...\n")

for link in linkages:
    for k in k_values:
        for m in metrics[link]:

            if link == "ward" and m != "euclidean":
                continue

            agg = AgglomerativeClustering(
                n_clusters=k,
                linkage=link,
                metric=m if link != "ward" else "euclidean"
            )

            
            labels = agg.fit_predict(X_sample)
            score = adjusted_rand_score(labels_true_sample, labels)

            print(f"k={k:2d} | link={link:8s} | metric={m:9s} | ARI={score:.4f}")

            if score > best_result["score"]:
                best_result["score"] = score
                best_result["params"] = (k, link, m)


print(f"Best ARI Score: {best_result['score']:.4f}")
print("k, linkage, metric:", best_result["params"])