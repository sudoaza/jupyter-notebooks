import pandas as pd

# Load your data
df = pd.read_csv('cleaned_data.csv')  # Replace with the path to your CSV file

# Calculate the threshold for minimum number of non-NA values in each column
# Half of the total number of rows
thresh = len(df) / 2

# Find columns where the number of NaN values is greater than the threshold
columns_with_many_nans = df.columns[df.isna().sum() > thresh]

# Display these columns
print(columns_with_many_nans)
