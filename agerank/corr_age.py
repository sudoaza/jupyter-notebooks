import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

df = pd.read_csv('cleaned_data.csv')

# Calculate correlations and p-values
correlations = {}
p_values = {}

for column in df.columns:
    if column != 'Age':
        df_temp = df.dropna(subset=[column], how="any")
        #correlation, p_value = stats.pearsonr(df_temp[column], df_temp['Age'])
        correlation, p_value = stats.spearmanr(df_temp[column], df_temp['Age'])
        correlations[column] = correlation
        p_values[column] = p_value

# Convert to DataFrame
correlations_df = pd.DataFrame.from_dict(correlations, orient='index', columns=['Correlation'])
correlations_df['p_value'] = pd.DataFrame.from_dict(p_values, orient='index')

# Filter out non-significant correlations
# Typically, a p-value of 0.05 or less is considered significant
significant_correlations = correlations_df[(correlations_df['p_value'] <= 0.05) & (abs(correlations_df['Correlation']) > 0.2)]
print(significant_correlations)

# Plotting the significant correlations
plt.figure(figsize=(15, 10))
plt.bar(significant_correlations.index, significant_correlations['Correlation'])
plt.xlabel('Biomarker')
plt.ylabel('Correlation with Age')
plt.title('Significant Correlations of Each Biomarker with Age')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

significant_biomarkers = significant_correlations.index
# Filter the original DataFrame to include only significant biomarkers
significant_df = df[significant_biomarkers]

significant_df.to_csv("significant_biomarkers.csv", index=False)

# Calculate the correlation matrix
corr_matrix = significant_df.corr(method='spearman')
print(corr_matrix)

annotate = len(significant_biomarkers) < 25

# Plotting the heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, cmap='coolwarm', annot=annotate)
plt.title('Heatmap of Correlation Between Significant Biomarkers')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# See which biomarkers are highly correlated with each other
high_corr_matrix = corr_matrix[corr_matrix.abs() > 0.80]
thresh = len(high_corr_matrix.columns)-1
high_corr_matrix = high_corr_matrix[high_corr_matrix.isna().sum() < thresh].dropna(axis=1,how="all")
print(high_corr_matrix)

# See from the redundants which ones are more correlated to age
redundant = high_corr_matrix.columns
print(correlations_df.loc[redundant])

# Now we want to check the original data to see for which we have more entries
df = pd.read_csv('merged_data.csv')
df[redundant].info()

# There is no significant difference between the number of entries or the most correlated is the most available
# So we keep the most correlated to age
# Body Mass Index                    0.263103   2.031736e-80 <-
# Weight (kg)                        0.230222   1.478312e-61

# Blood Mercury - Methyl (ug/L)      0.245638   1.182716e-70
# Blood Mercury - Total (ug/L)       0.264675   4.164345e-82 <-

# Blood Pressure - Max Inflation     0.636197   0.000000e+00 <-
# Blood Pressure - Systolic          0.575088   0.000000e+00

# Mean Cell Hemoglobin (pg)          0.253893   1.576355e-75
# Mean Cell Volume (fL)              0.313840  1.820120e-116 <-

# Cholesterol - Total (mg/dL)        0.287630   4.472882e-97 <-
# Serum Cholesterol                  0.274162   4.561473e-86

# Vitamin D HD3                      0.278938   2.010638e-91
# Vitamin D Both                     0.336266  1.710769e-134 <-
# Vitamin D Epi HD3                  0.223113   2.970909e-58

# ["Body Mass Index","Blood Cadmium (ug/L)","Blood Lead (ug/dL)","Blood Mercury - Total (ug/L)","Blood Pressure - Diastolic","Blood Pressure - Max Inflation","Blood Pressure - BPM (beats/min)","Mean Cell Volume (fL)","Mean Platelet Count (1000 cells/uL)","Red Cell Distribution Width (%)","Cholesterol - Total (mg/dL)","Ferritin (ug/L)","Glycohemoglobin A1c (%)","High Sensitivity C Reactive Protein","Blood Urea Nitrogen (mg/dL)","Gamma-Glutamyl Transferase (IU/L)","Osmolality (mmol/Kg)","Phosphorous (mg/dL)","Serum Albumin","Serum Glucose","Serum Triglycerides","Serum Unsaturated Iron Binding","Vitamins - Tocopherol","Vitamin D Both","Vitamins - Cis Beta Carotene","Vitamins - Retinol"]