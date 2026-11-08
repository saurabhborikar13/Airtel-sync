import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score

leads_path = r"d:\Airtel_prj\extracted_input\YTL_TrackA_Udyam_Digital_Data\smb_leads.csv"
df = pd.read_csv(leads_path)

df["target"] = (df["outcome"] == "Activated").astype(int)
print(f"Dataset shape: {df.shape}")
print(f"Target distribution:\n{df['target'].value_counts(normalize=True)}")

features = [
    "lead_source", "segment", "city_tier", "state", "preferred_language",
    "employee_count", "num_sites", "annual_turnover_band",
    "has_gstin", "has_udyam", "current_internet", "monthly_telecom_spend_inr"
]

X = df[features].copy()
y = df["target"]

X["monthly_telecom_spend_inr"] = X["monthly_telecom_spend_inr"].fillna(X["monthly_telecom_spend_inr"].median())
X["employee_count"] = X["employee_count"].fillna(X["employee_count"].median())
X["num_sites"] = X["num_sites"].fillna(1)

categorical_cols = [
    "lead_source", "segment", "city_tier", "state", "preferred_language",
    "annual_turnover_band", "has_gstin", "has_udyam", "current_internet"
]
numeric_cols = ["employee_count", "num_sites", "monthly_telecom_spend_inr"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ]
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model.fit(X_train, y_train)

y_pred_proba = model.predict_proba(X_test)[:, 1]
y_pred = model.predict(X_test)

print(f"ROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

os.makedirs(r"d:\Airtel_prj\models", exist_ok=True)
with open(r"d:\Airtel_prj\models\propensity_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to d:\\Airtel_prj\\models\\propensity_model.pkl")
