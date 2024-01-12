import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import RobustScaler
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
df = pd.read_csv('cleaned_data.csv')  # Replace with your CSV file path

# Selecting only the biomarker columns (assuming SEQN and Age are not part of PCA)
biomarkers = df.drop(['SEQN', 'Age'], axis=1)

# Handle missing values
biomarkers = biomarkers.fillna(biomarkers.mean())

# Standardize the data
scaler = RobustScaler()
biomarkers_scaled = scaler.fit_transform(biomarkers)

# Apply PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(biomarkers_scaled)

# Create a DataFrame with the principal components
pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

# Add the 'Age' column for coloring
pca_df['Age'] = df['Age']

# Plotting the 2D scatter plot with Age as color
plt.figure(figsize=(8, 6))
scatter = plt.scatter(pca_df['PC1'], pca_df['PC2'], c=pca_df['Age'], cmap='Spectral_r', s=15, edgecolor='none', alpha=0.7)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('2D PCA of Biomarkers with Age Coloring')
plt.colorbar(scatter, label='Age')
plt.show()

# Extracting PCA Loadings
loadings = pd.DataFrame(pca.components_.T, columns=['PC1', 'PC2'], index=biomarkers.columns)

# Display the top contributing features for each component
print("Top contributing features for PC1:")
print(loadings['PC1'].sort_values(ascending=False).head(5))

print("\nTop contributing features for PC2:")
print(loadings['PC2'].sort_values(ascending=False).head(5))
