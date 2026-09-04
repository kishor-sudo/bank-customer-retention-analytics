"""
Phase 6 — Predictive Layer (optional but recommended)
Customer Engagement & Product Utilization Analytics for Retention Strategy
"""
 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
 
SEGMENTED_PATH = "data/segmented_churn.csv"
IMPORTANCE_CHART_PATH = "outputs/phase6_feature_importances.png"
CONFUSION_CHART_PATH = "outputs/phase6_confusion_matrix.png"
 
df = pd.read_csv(SEGMENTED_PATH)
 
# ---------------------------------------------------------------
# 1. Feature prep — encode categoricals
# ---------------------------------------------------------------
feature_cols = [
    "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts",
    "HasCrCard", "IsActiveMember", "EstimatedSalary", "CreditScore"
]
target_col = "Exited"
 
model_df = df[feature_cols + [target_col]].copy()
 
# Encode categoricals
le_geo = LabelEncoder()
le_gender = LabelEncoder()
model_df["Geography"] = le_geo.fit_transform(model_df["Geography"])
model_df["Gender"] = le_gender.fit_transform(model_df["Gender"])
 
print("=" * 70)
print("1. FEATURE PREP")
print("=" * 70)
print(f"Features used: {feature_cols}")
print(f"Geography encoding: {dict(zip(le_geo.classes_, le_geo.transform(le_geo.classes_)))}")
print(f"Gender encoding: {dict(zip(le_gender.classes_, le_gender.transform(le_gender.classes_)))}")
 
X = model_df[feature_cols]
y = model_df[target_col]
 
# ---------------------------------------------------------------
# 2. Train/test split + Random Forest
# ---------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain size: {len(X_train)}  |  Test size: {len(X_test)}")
print(f"Train churn rate: {y_train.mean()*100:.2f}%  |  Test churn rate: {y_test.mean()*100:.2f}%")
 
model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42, class_weight="balanced")
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
 
# ---------------------------------------------------------------
# 3. Metrics
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("3. MODEL PERFORMANCE")
print("=" * 70)
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
print(f"Accuracy:  {acc*100:.2f}%")
print(f"Precision (Exited=1): {prec*100:.2f}%")
print(f"Recall (Exited=1):    {rec*100:.2f}%")
print(f"\nNote: churn class (~20% of data) is imbalanced. Accuracy alone is misleading here —")
print(f"a model that always predicts 'stayed' would score ~80% accuracy while catching zero churners.")
print(f"Precision/recall on the minority (Exited=1) class are the meaningful numbers.")
 
print("\nFull classification report:")
print(classification_report(y_test, y_pred, target_names=["Stayed (0)", "Exited (1)"]))
 
cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix:")
print(f"                 Predicted Stayed  Predicted Exited")
print(f"Actual Stayed         {cm[0][0]:>6}            {cm[0][1]:>6}")
print(f"Actual Exited         {cm[1][0]:>6}            {cm[1][1]:>6}")
 
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(cm, cmap="Blues")
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(["Predicted Stayed", "Predicted Exited"])
ax.set_yticklabels(["Actual Stayed", "Actual Exited"])
for i in range(2):
    for j in range(2):
        ax.text(j, i, str(cm[i][j]), ha="center", va="center",
                color="white" if cm[i][j] > cm.max()/2 else "black", fontsize=14)
ax.set_title("Confusion Matrix — Churn Prediction")
plt.colorbar(im, ax=ax)
plt.tight_layout()
plt.savefig(CONFUSION_CHART_PATH, dpi=150)
plt.close()
print(f"\nConfusion matrix chart saved to: {CONFUSION_CHART_PATH}")
 
# ---------------------------------------------------------------
# 4. Feature importances
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("4. FEATURE IMPORTANCES")
print("=" * 70)
importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
print(importances.round(4))
 
fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(importances.index[::-1], importances.values[::-1], color="#2980b9")
ax.set_xlabel("Feature Importance")
ax.set_title("Random Forest Feature Importances — Churn Prediction")
plt.tight_layout()
plt.savefig(IMPORTANCE_CHART_PATH, dpi=150)
plt.close()
print(f"\nChart saved to: {IMPORTANCE_CHART_PATH}")
 
print("\nTop 3 features:")
for feat, val in importances.head(3).items():
    print(f"  {feat}: {val:.4f}")
 