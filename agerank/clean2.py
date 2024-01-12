import pandas as pd

final_biomarkers = [
# This were correlated with age but were heavily skewed
#   "Blood Cadmium (ug/L)",
#   "Blood Lead (ug/dL)",
#   "Blood Mercury - Total (ug/L)",
#   "Ferritin (ug/L)",
#   "Vitamins - Cis Beta Carotene",
#   "Gamma-Glutamyl Transferase (IU/L)",
#   "High Sensitivity C Reactive Protein",
#   "Serum Glucose", # CMP
#   "Serum Triglycerides", # Lipid Panel
#   "Glycohemoglobin A1c (%)",
# /skewed end
#   "DXA Visceral Fat Volume", # correlated with BMI ok and expensive
"Body Mass Index",
"Blood Pressure - Diastolic",
"Blood Pressure - Max Inflation",
"Blood Pressure - BPM (beats/min)",
"Mean Cell Volume (fL)",
"Mean Platelet Count (1000 cells/uL)",
"Red Cell Distribution Width (%)",
"Cholesterol - Total (mg/dL)",
"Blood Urea Nitrogen (mg/dL)",
#"Osmolality (mmol/Kg)", # too expensive
"Phosphorous (mg/dL)",
"Serum Albumin",
"Serum Unsaturated Iron Binding",
"Vitamins - Tocopherol",
"Vitamin D Both",
#"Vitamins - Retinol" # too expensive
]

keep_cols = ["SEQN", "Age"] + final_biomarkers

df = pd.read_csv('merged_data.csv', usecols=keep_cols)

# Outliers
df = df[~df.SEQN.isin([93923, 94275, 94314, 96086, 98776, 100305, 100717, 100987, 101149, 101175, 102179, 102726, 102836, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956, 102956])]

# 90% of the columns must have a valueor we drop them
df.dropna(thresh=len(keep_cols) * 0.8, inplace=True)

df.to_csv('cleaned_data.csv', index=False)
