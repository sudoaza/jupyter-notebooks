import pandas as pd

# Load your data
df = pd.read_csv('merged_data.csv')  # Replace with your CSV file path

df.dropna(thresh=len(df.columns) * 1 / 3, inplace=True)
df.dropna(thresh=len(df)* 1/4, axis=1, inplace=True)

df.dropna(thresh=len(df)/2, axis=1, inplace=True)
df.dropna(thresh=len(df.columns) * 2 / 3, inplace=True)

# Save the cleaned DataFrame (optional)
df.to_csv('cleaned_data.csv', index=False)
