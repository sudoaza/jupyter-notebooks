import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import RobustScaler
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('cleaned_data.csv')  # Replace with your CSV file path

# Selecting only the biomarker columns
biomarkers = df.drop(['SEQN', 'Age'], axis=1)

# Handle missing values
biomarkers = biomarkers.fillna(biomarkers.mean())

# Standardize the data
scaler = RobustScaler()
biomarkers_scaled = scaler.fit_transform(biomarkers)

# Applying PCA
pca = PCA()
pca.fit(biomarkers_scaled)

# Cumulative explained variance ratio as a function of the number of components
cumulative_variance_ratio = pca.explained_variance_ratio_.cumsum()

# Plotting the explained variances
plt.figure(figsize=(8, 6))
plt.plot(range(1, len(cumulative_variance_ratio) + 1), cumulative_variance_ratio, marker='o')
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('Elbow Method for Optimal Number of Principal Components')
plt.grid(True)
plt.show()
