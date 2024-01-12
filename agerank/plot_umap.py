import pandas as pd
import umap
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import RobustScaler

# Load the CSV file
df = pd.read_csv('cleaned_data.csv')  # Replace with your CSV file path

# Selecting only the biomarker columns
biomarkers = df.drop(['SEQN', 'Age'], axis=1)

# Handle missing values
biomarkers = biomarkers.fillna(biomarkers.mean())

# Standardize the data
scaler = RobustScaler()
biomarkers_scaled = scaler.fit_transform(biomarkers)

# UMAP projection to 2 dimensions
reducer = umap.UMAP(n_components=2, random_state=42)
embedding = reducer.fit_transform(biomarkers_scaled)

# for marker in biomarkers.columns.values.tolist() + ["Age"]:
for marker in ["Age"]:
  # Plotting the 2D scatter plot
  plt.figure(figsize=(12, 8))
  plt.scatter(embedding[:, 0], embedding[:, 1], c=df[marker], cmap='Spectral_r', s=4)
  plt.colorbar(label=marker)
  plt.title('2D UMAP Projection of Biomarkers')
  plt.xlabel('UMAP1')
  plt.ylabel('UMAP2')
  plt.grid(True)
  plt.show()

# Reduce dimensions with UMAP
reducer = umap.UMAP(random_state=42)
embedding = reducer.fit_transform(biomarkers_scaled)

# Cluster with DBSCAN
db = DBSCAN(eps=0.5, min_samples=5)
clusters = db.fit_predict(embedding)

# Plot clusters
plt.scatter(embedding[:, 0], embedding[:, 1], c=clusters, cmap='Spectral', s=50)
plt.title('Clusters of Biomarkers')
plt.xlabel('UMAP 1')
plt.ylabel('UMAP 2')
plt.colorbar(label='Cluster Label')
plt.show()

df["cluster"] = clusters
df.to_csv("clusters.csv", index=False)
