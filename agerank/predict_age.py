import pandas as pd
import matplotlib.pyplot as plt
import xgboost as xgb
import shap
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import RobustScaler
import scipy.stats as stats

df = pd.read_csv('cleaned_data.csv')

# Selecting only the biomarker columns
biomarkers = df.drop(['SEQN', 'Age'], axis=1)
# Handle missing values
biomarkers = biomarkers.fillna(biomarkers.mean())
# Standardize the data
scaler = RobustScaler()
X = scaler.fit_transform(biomarkers)
y = df['Age']

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = xgb.XGBRegressor(objective='reg:squarederror')
model.fit(X_train, y_train)

# Predictions and evaluation
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")
correlation, p_value = stats.spearmanr(y_test, y_pred)
print(f"Correlation: {correlation}, p-value: {p_value}")

# SHAP Values
explainer = shap.Explainer(model)
shap_values = explainer(X_train)

# Plot SHAP summary
shap.summary_plot(shap_values, X_train, feature_names=biomarkers.columns.tolist())


# Train predictions
y_train_pred = model.predict(X_train)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(y_train, y_train_pred, color='red', alpha=0.5, label='Train Data')
plt.scatter(y_test, y_pred, color='green', alpha=0.5, label='Test Data')
plt.title('Actual vs. Predicted Age')
plt.xlabel('Actual Age')
plt.ylabel('Predicted Age')
plt.legend()
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--')  # Diagonal line for reference
plt.show()