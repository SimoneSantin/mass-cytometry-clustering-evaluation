from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

data_markers = pd.read_csv("human_blood_mass_cytometry_batch1.csv", index_col=0)
data_celltypes = pd.read_csv("human_blood_mass_cytometry_batch1_metadata.csv") 
labels_true = data_celltypes["cell_type"].values

X = data_markers.values
y = labels_true  

# Riduzione dimensionale con t-SNE
tsne = TSNE(n_components=2, random_state=42, perplexity=30, learning_rate=200)
X_tsne = tsne.fit_transform(X)

unique_labels = np.unique(y)
colors = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())
palette = {label: colors[i % len(colors)] for i, label in enumerate(unique_labels)}

# Plot
fig, ax = plt.subplots(dpi=180, figsize=(6,6))

for label in unique_labels:
    ax.scatter(
        X_tsne[y == label, 0],
        X_tsne[y == label, 1],
        s=5,
        label=label,
        c=palette[label]
    )

ax.tick_params(axis='both', which='major', labelsize=6)
ax.legend(bbox_to_anchor=(1.05, 1), markerscale=2.5, fontsize=6)
ax.set_xlabel('t-SNE1')
ax.set_ylabel('t-SNE2')
ax.set_title('Flow Cytometry t-SNE (2D)')
plt.tight_layout()
plt.savefig('tsneReduction.png')
