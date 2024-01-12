import pandas as pd
import numpy as np
import umap
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import RobustScaler

# Load the CSV file
df = pd.read_csv('cleaned_data.csv')  # Replace with your CSV file path

# Drop non-biomarker columns
biomarkers_df = df.drop(['SEQN', 'Age'], axis=1)
biomarkers_df = biomarkers_df.fillna(biomarkers_df.mean())

# Transpose the DataFrame to get biomarkers as rows
biomarkers_df = biomarkers_df.transpose()

# Standardize the data
scaler = RobustScaler()
biomarkers_scaled = scaler.fit_transform(biomarkers_df)

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
