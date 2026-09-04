"""
Phase 2 — Engagement Classification
Customer Engagement & Product Utilization Analytics for Retention Strategy
"""
 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
CLEANED_PATH = "data/cleaned_churn.csv"
SEGMENTED_PATH = "data/segmented_churn.csv"
CHART_PATH = "outputs/phase2_churn_by_engagement_profile.png"
 
df = pd.read_csv(CLEANED_PATH)
 
# ---------------------------------------------------------------
# Build EngagementProfile — first-match-wins, in the stated order
# ---------------------------------------------------------------
balance_p75 = df["Balance"].quantile(0.75)
print(f"75th percentile of Balance: {balance_p75:,.2f}")
 
def classify(row):
    if row["IsActiveMember"] == 1 and row["NumOfProducts"] >= 2:
        return "Active Engaged"
    if row["IsActiveMember"] == 0 and row["NumOfProducts"] == 1:
        return "Inactive Disengaged"
    if row["IsActiveMember"] == 1 and row["NumOfProducts"] == 1:
        return "Active Low-Product"
    if row["IsActiveMember"] == 0 and row["Balance"] >= balance_p75:
        return "Inactive High-Balance"
    return "Unclassified"
 
df["EngagementProfile"] = df.apply(classify, axis=1)
 
# ---------------------------------------------------------------
# Report any customers falling outside all four rules
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("UNCLASSIFIED CHECK")
print("=" * 70)
unclassified = df[df["EngagementProfile"] == "Unclassified"]
print(f"Unclassified customers: {len(unclassified)}")
if len(unclassified) > 0:
    print("These are IsActiveMember=0, NumOfProducts>=2, and Balance below the 75th percentile —")
    print("i.e. inactive multi-product customers who aren't high-balance. Assigning them to")
    print("'Inactive Disengaged' since they share the core disengagement trait (inactive), just")
    print("with more than one product.")
    df.loc[df["EngagementProfile"] == "Unclassified", "EngagementProfile"] = "Inactive Disengaged"
else:
    print("All customers matched one of the four defined rules — no fallback needed.")
 
# ---------------------------------------------------------------
# 1. Count and % per segment
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("1. SEGMENT SIZE (COUNT & %)")
print("=" * 70)
segment_counts = df["EngagementProfile"].value_counts()
segment_pct = df["EngagementProfile"].value_counts(normalize=True) * 100
segment_summary = pd.DataFrame({
    "Count": segment_counts,
    "Percent": segment_pct.round(1)
})
print(segment_summary)
 
# ---------------------------------------------------------------
# 2. Churn rate per segment
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("2. CHURN RATE BY SEGMENT")
print("=" * 70)
churn_by_segment = df.groupby("EngagementProfile")["Exited"].mean().mul(100).round(2)
churn_by_segment = churn_by_segment.sort_values(ascending=False)
print(churn_by_segment.to_string())
 
overall_churn = df["Exited"].mean() * 100
print(f"\n(Reference — overall churn rate across all customers: {overall_churn:.2f}%)")
 
# ---------------------------------------------------------------
# 3. Bar chart — churn rate by segment, sorted highest to lowest
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))
colors = ["#c0392b" if v > overall_churn else "#2980b9" for v in churn_by_segment.values]
bars = ax.bar(churn_by_segment.index, churn_by_segment.values, color=colors)
ax.axhline(overall_churn, color="gray", linestyle="--", linewidth=1,
           label=f"Overall churn rate ({overall_churn:.1f}%)")
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Engagement Profile")
ax.set_xticklabels(churn_by_segment.index, rotation=20, ha="right")
for bar, val in zip(bars, churn_by_segment.values):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.5, f"{val:.1f}%",
            ha="center", va="bottom", fontsize=9)
ax.legend()
plt.tight_layout()
plt.savefig(CHART_PATH, dpi=150)
print(f"\nChart saved to: {CHART_PATH}")
 
# ---------------------------------------------------------------
# 4. Save updated dataset
# ---------------------------------------------------------------
df.to_csv(SEGMENTED_PATH, index=False)
print("\n" + "=" * 70)
print("4. SAVED SEGMENTED DATASET")
print("=" * 70)
print(f"Saved to: {SEGMENTED_PATH}")
print(f"Shape: {df.shape}")
 
# ---------------------------------------------------------------
# 5. Interpretation
# ---------------------------------------------------------------
highest_seg = churn_by_segment.idxmax()
highest_val = churn_by_segment.max()
lowest_seg = churn_by_segment.idxmin()
lowest_val = churn_by_segment.min()
 
print("\n" + "=" * 70)
print("5. INTERPRETATION")
print("=" * 70)
print(f"Highest-churning segment: {highest_seg} ({highest_val:.1f}%)")
print(f"Lowest-churning segment: {lowest_seg} ({lowest_val:.1f}%)")
