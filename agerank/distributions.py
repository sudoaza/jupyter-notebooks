import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file
#df = pd.read_csv('cleaned_data.csv')
df = pd.read_csv('significant_biomarkers.csv')

# Selecting only the biomarker columns
biomarkers = df
try:
    biomarkers = df.drop(['SEQN'], axis=1)
except:
    pass

# Handle missing values
biomarkers = biomarkers.fillna(biomarkers.mean())

print("All Biomarkers")
print("Marker                               Mean                Std                 Skewness")
for marker in biomarkers.columns:
    #sns.displot(df, x=marker)
    col = df[marker]
    print("{: >35} {: >20} {: >20} {: >20}".format(marker, col.mean(), col.std(), col.skew()))
    #plt.show()

print("Non Skewed")
print("Marker                               Mean                Std                 Skewness")
for marker in biomarkers.columns:
    col = df[marker]
    if abs(col.skew()) > 3:
        continue
    print("{: >35} {: >20} {: >20} {: >20}".format(marker, col.mean(), col.std(), col.skew()))
