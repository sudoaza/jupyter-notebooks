import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
df = pd.read_csv('clusters.csv')  # Replace with your CSV file path

df.info()
# Remove non-biomarker columns (like 'SEQN' and 'Age') and keep the cluster column
biomarkers = df.drop(['SEQN', 'Age'], axis=1)

biomarkers = biomarkers.fillna(biomarkers.mean())

# Perform ANOVA or Kruskal-Wallis test for each biomarker
anova_results = {}
kruskal_results = {}

for biomarker in biomarkers.columns.drop('cluster'):
    groups = [group[1] for group in biomarkers.groupby('cluster')[biomarker]]
    
    # ANOVA Test
    f_val, p_val_anova = stats.f_oneway(*groups)
    anova_results[biomarker] = p_val_anova

    # Kruskal-Wallis Test
    _, p_val_kruskal = stats.kruskal(*groups)
    kruskal_results[biomarker] = p_val_kruskal

# Convert results to DataFrame
anova_df = pd.DataFrame.from_dict(anova_results, orient='index', columns=['ANOVA_p_value'])
kruskal_df = pd.DataFrame.from_dict(kruskal_results, orient='index', columns=['Kruskal_p_value'])

# Combine results
results_df = anova_df.join(kruskal_df)

results_df["combined_significance"] = results_df['ANOVA_p_value'] * results_df['Kruskal_p_value']

# Filter by significance level, e.g., p-value < 0.05
significant_anova = results_df[results_df['ANOVA_p_value'] < 0.05]
significant_kruskal = results_df[results_df['Kruskal_p_value'] < 0.05]

print("Significant Biomarkers (ANOVA):")
print(significant_anova)

print("\nSignificant Biomarkers (Kruskal-Wallis):")
print(significant_kruskal)

# Optional: Plotting significant biomarkers
# This is a simple bar plot for demonstration. You may want to create more informative visualizations.
plt.figure(figsize=(10, 5))
plt.bar(significant_anova.index, significant_anova['ANOVA_p_value'])
plt.xticks(rotation=45, ha='right')
plt.xlabel('Biomarker')
plt.ylabel('ANOVA p-value')
plt.title('Significant Biomarkers - ANOVA Test')
plt.tight_layout()
plt.show()

# Identify the two most significant biomarkers
two_most_significant = results_df['ANOVA_p_value'].nsmallest(2).index
#two_most_significant = ["Blood Cadmium (ug/L)", "Ferritin (ug/L)"]
# Extracting these biomarkers and the cluster column
plot_data = df[[*two_most_significant, 'cluster']]


# Creating the scatter plot
plt.figure(figsize=(10, 8))
sns.scatterplot(data=plot_data, x=two_most_significant[0], y=two_most_significant[1], hue='cluster', palette='viridis')
plt.title(f'Scatter Plot of {two_most_significant[0]} vs {two_most_significant[1]} by Cluster')
plt.xlabel(two_most_significant[0])
plt.ylabel(two_most_significant[1])
plt.legend(title='Cluster', loc='upper right')
plt.show()
