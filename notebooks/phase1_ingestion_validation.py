"""
Phase 1 — Setup + Data Ingestion & Validation
Customer Engagement & Product Utilization Analytics for Retention Strategy
"""
 
import pandas as pd
import numpy as np
 
RAW_PATH = "data/European_Bank.csv"
CLEANED_PATH = "data/cleaned_churn.csv"
 
# ---------------------------------------------------------------
# 1. Load dataset and confirm shape, dtypes, columns
# ---------------------------------------------------------------
df = pd.read_csv(RAW_PATH)
print("=" * 70)
print("1. SHAPE, DTYPES, COLUMNS")
print("=" * 70)
print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"\nColumns: {list(df.columns)}")
print(f"\nDtypes:\n{df.dtypes}")
 
# ---------------------------------------------------------------
# 2. Missing values + duplicate CustomerId
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("2. MISSING VALUES & DUPLICATE CUSTOMERID")
print("=" * 70)
null_counts = df.isnull().sum()
total_nulls = null_counts.sum()
print(f"Total missing values: {total_nulls}")
if total_nulls > 0:
    print(null_counts[null_counts > 0])
else:
    print("No missing values found in any column.")
 
dup_count = df["CustomerId"].duplicated().sum()
print(f"\nDuplicate CustomerId rows: {dup_count}")
if dup_count == 0:
    print("Confirmed: CustomerId is unique across all rows.")
 
# ---------------------------------------------------------------
# 3. Validate binary columns
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("3. BINARY COLUMN VALIDATION (HasCrCard, IsActiveMember, Exited)")
print("=" * 70)
binary_cols = ["HasCrCard", "IsActiveMember", "Exited"]
for col in binary_cols:
    unique_vals = sorted(df[col].unique())
    is_valid = set(unique_vals).issubset({0, 1})
    print(f"{col}: unique values = {unique_vals} -> {'VALID (strictly 0/1)' if is_valid else 'INVALID'}")
 
# ---------------------------------------------------------------
# 4. Validate NumOfProducts range
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("4. NUMOFPRODUCTS RANGE VALIDATION")
print("=" * 70)
prod_min, prod_max = df["NumOfProducts"].min(), df["NumOfProducts"].max()
prod_vals = sorted(df["NumOfProducts"].unique())
print(f"NumOfProducts unique values: {prod_vals}")
print(f"Range: {prod_min}-{prod_max}")
in_expected_range = df["NumOfProducts"].between(1, 4).all()
print(f"All values within expected 1-4 range: {in_expected_range}")
 
# ---------------------------------------------------------------
# 5. Drop Year column (constant, not analytically useful)
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("5. YEAR COLUMN")
print("=" * 70)
year_unique = df["Year"].unique()
print(f"Year unique values: {year_unique}")
if len(year_unique) == 1:
    print(f"Year is constant at {year_unique[0]} across all {len(df)} rows.")
    print("Decision: dropping Year — it carries no variance and cannot support trend")
    print("or cohort analysis. Retained implicitly as a 'data snapshot date' note only.")
    df = df.drop(columns=["Year"])
else:
    print("Year varies — NOT dropping. Review before proceeding.")
 
# ---------------------------------------------------------------
# 6. Balance = 0 check
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("6. ZERO-BALANCE ACCOUNTS")
print("=" * 70)
zero_balance_count = (df["Balance"] == 0).sum()
zero_balance_pct = zero_balance_count / len(df) * 100
print(f"Rows with Balance = 0: {zero_balance_count} ({zero_balance_pct:.1f}% of dataset)")
print("These are treated as real zero-balance accounts (e.g. customers who hold only")
print("a card/loan product with no deposit balance), NOT missing data. No imputation applied.")
 
# Sanity check: are zero-balance customers disproportionately churners?
zero_bal_churn = df.loc[df["Balance"] == 0, "Exited"].mean() * 100
nonzero_bal_churn = df.loc[df["Balance"] != 0, "Exited"].mean() * 100
print(f"\nChurn rate when Balance=0: {zero_bal_churn:.1f}%")
print(f"Churn rate when Balance>0: {nonzero_bal_churn:.1f}%")
 
# ---------------------------------------------------------------
# Overall churn rate (baseline reference for later phases)
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("BASELINE: OVERALL CHURN RATE")
print("=" * 70)
overall_churn = df["Exited"].mean() * 100
print(f"Overall churn rate: {overall_churn:.2f}% ({df['Exited'].sum()} of {len(df)} customers)")
 
# ---------------------------------------------------------------
# 7. Save cleaned dataset
# ---------------------------------------------------------------
df.to_csv(CLEANED_PATH, index=False)
print("\n" + "=" * 70)
print("7. SAVED CLEANED DATASET")
print("=" * 70)
print(f"Saved to: {CLEANED_PATH}")
print(f"Final shape: {df.shape}")
print(f"Final columns: {list(df.columns)}")
 