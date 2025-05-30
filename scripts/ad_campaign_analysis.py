# scripts/ad_campaign_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Step 1: Load the data
df = pd.read_csv('data/processed/ads_cleaned.csv')

# Step 2: Basic cleanup
df.drop(columns=['id', 'full_name'], inplace=True)
df.dropna(inplace=True)

# Step 3: Convert categorical to numeric
df_encoded = pd.get_dummies(df, drop_first=True)

# Step 4: Split features and target
X = df_encoded.drop('click', axis=1)
y = df_encoded['click']

# Step 5: Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 7: Make predictions and evaluate
y_pred = model.predict(X_test)

print("\n🎯 Classification Report:\n")
print(classification_report(y_test, y_pred))

print("\n🌀 Confusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))

# Step 8: Feature Importance
feature_imp = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=feature_imp, y=feature_imp.index)
plt.title("🔥 Feature Importance in Ad Click Prediction")
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.tight_layout()
plt.show()

# ✅ Step 9: Save predictions to a CSV file (with actual + predicted clicks)
df_results = X_test.copy()
df_results['actual_click'] = y_test.values
df_results['predicted_click'] = y_pred
df_results.to_csv('data/processed/ad_campaign_predictions.csv', index=False)
print("\n✅ ad_campaign_predictions.csv saved to data/processed/")
