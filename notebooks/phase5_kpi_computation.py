"""
Phase 5 — Retention Strength Assessment & KPI Computation
Customer Engagement & Product Utilization Analytics for Retention Strategy
"""
 
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
sys.path.append(".")
from src.kpis import (
    engagement_retention_ratio,
    product_depth_index,
    high_balance_disengagement_rate,
    credit_card_stickiness_score,
    relationship_strength_index,
)
 
SEGMENTED_PATH = "data/segmented_churn.csv"
KPI_SUMMARY_PATH = "outputs/kpi_summary.csv"
RSI_CHART_PATH = "outputs/phase5_rsi_churn_by_quartile.png"
 
df = pd.read_csv(SEGMENTED_PATH)
geographies = sorted(df["Geography"].unique())
 
summary_rows = []
 
# ---------------------------------------------------------------
# 1. Engagement Retention Ratio
# ---------------------------------------------------------------
print("=" * 70)
print("1. ENGAGEMENT RETENTION RATIO")
print("=" * 70)
err_overall = engagement_retention_ratio(df)
print(f"Overall: {err_overall:.2f}x  (inactive customers churn {err_overall:.2f}x more than active)")
summary_rows.append({"KPI": "Engagement Retention Ratio", "Breakdown": "Overall", "Value": round(err_overall, 2)})
 
print("\nBy Geography:")
for geo in geographies:
    val = engagement_retention_ratio(df[df["Geography"] == geo])
    print(f"  {geo}: {val:.2f}x")
    summary_rows.append({"KPI": "Engagement Retention Ratio", "Breakdown": geo, "Value": round(val, 2)})
 
# ---------------------------------------------------------------
# 2. Product Depth Index
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("2. PRODUCT DEPTH INDEX")
print("=" * 70)
pdi_overall = product_depth_index(df)
direction = "POSITIVE (more products -> higher churn, contradicts naive assumption)" if pdi_overall > 0 else "negative (more products -> lower churn, as naively expected)"
print(f"Overall: {pdi_overall:.3f}  -> {direction}")
summary_rows.append({"KPI": "Product Depth Index", "Breakdown": "Overall", "Value": round(pdi_overall, 3)})
 
print("\nBy Geography:")
for geo in geographies:
    val = product_depth_index(df[df["Geography"] == geo])
    print(f"  {geo}: {val:.3f}")
    summary_rows.append({"KPI": "Product Depth Index", "Breakdown": geo, "Value": round(val, 3)})
 
# ---------------------------------------------------------------
# 3. High-Balance Disengagement Rate
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("3. HIGH-BALANCE DISENGAGEMENT RATE")
print("=" * 70)
hbdr_overall = high_balance_disengagement_rate(df)
print(f"Overall: {hbdr_overall:.1f}% of top-quartile-balance customers are inactive")
summary_rows.append({"KPI": "High-Balance Disengagement Rate (%)", "Breakdown": "Overall", "Value": round(hbdr_overall, 1)})
 
print("\nBy Geography (using each geography's own top-quartile threshold):")
for geo in geographies:
    val = high_balance_disengagement_rate(df[df["Geography"] == geo])
    print(f"  {geo}: {val:.1f}%")
    summary_rows.append({"KPI": "High-Balance Disengagement Rate (%)", "Breakdown": geo, "Value": round(val, 1)})
 
# ---------------------------------------------------------------
# 4. Credit Card Stickiness Score
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("4. CREDIT CARD STICKINESS SCORE")
print("=" * 70)
ccss_overall = credit_card_stickiness_score(df)
direction = "cards ARE sticky (lower churn)" if ccss_overall > 0 else "cards are NOT sticky (no churn benefit, or higher churn)"
print(f"Overall: {ccss_overall:+.2f} percentage points -> {direction}")
summary_rows.append({"KPI": "Credit Card Stickiness Score (pp)", "Breakdown": "Overall", "Value": round(ccss_overall, 2)})
 
print("\nBy Geography:")
for geo in geographies:
    val = credit_card_stickiness_score(df[df["Geography"] == geo])
    print(f"  {geo}: {val:+.2f} pp")
    summary_rows.append({"KPI": "Credit Card Stickiness Score (pp)", "Breakdown": geo, "Value": round(val, 2)})
 
# ---------------------------------------------------------------
# 5. Relationship Strength Index — compute + validate against churn
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("5. RELATIONSHIP STRENGTH INDEX")
print("=" * 70)
df["RelationshipStrengthIndex"] = relationship_strength_index(df)
print(df["RelationshipStrengthIndex"].describe().round(3))
 
df["RSI_Quartile"] = pd.qcut(
    df["RelationshipStrengthIndex"].rank(method="first"), 4,
    labels=["Q1 (Weakest)", "Q2", "Q3", "Q4 (Strongest)"]
)
rsi_churn = df.groupby("RSI_Quartile", observed=True)["Exited"].mean() * 100
print("\nChurn rate by Relationship Strength Index quartile:")
print(rsi_churn.round(2))
 
monotonic_decreasing = all(
    rsi_churn.values[i] >= rsi_churn.values[i + 1] for i in range(len(rsi_churn) - 1)
)
print(f"\nMonotonically decreasing (stronger relationship -> lower churn, as intended): {monotonic_decreasing}")
 
for quartile, val in rsi_churn.items():
    summary_rows.append({"KPI": "RSI Churn Rate by Quartile (%)", "Breakdown": quartile, "Value": round(val, 2)})
 
# Chart
fig, ax = plt.subplots(figsize=(8, 6))
overall_churn = df["Exited"].mean() * 100
colors = ["#c0392b" if v > overall_churn else "#2980b9" for v in rsi_churn.values]
bars = ax.bar(rsi_churn.index, rsi_churn.values, color=colors)
ax.axhline(overall_churn, color="gray", linestyle="--", linewidth=1,
           label=f"Overall churn rate ({overall_churn:.1f}%)")
for bar, val in zip(bars, rsi_churn.values):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.5, f"{val:.1f}%",
            ha="center", va="bottom", fontsize=9)
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Relationship Strength Index Quartile")
ax.legend()
plt.tight_layout()
plt.savefig(RSI_CHART_PATH, dpi=150)
plt.close()
print(f"\nChart saved to: {RSI_CHART_PATH}")
 
# ---------------------------------------------------------------
# Save KPI summary table
# ---------------------------------------------------------------
kpi_summary_df = pd.DataFrame(summary_rows)
kpi_summary_df.to_csv(KPI_SUMMARY_PATH, index=False)
print("\n" + "=" * 70)
print("SAVED KPI SUMMARY")
print("=" * 70)
print(f"Saved to: {KPI_SUMMARY_PATH}")
print(f"Rows: {len(kpi_summary_df)}")
 
# Also save the dataset with RSI columns added, for use in the dashboard later
df.to_csv("data/segmented_churn_with_rsi.csv", index=False)
print(f"Also saved dataset with RSI columns to: data/segmented_churn_with_rsi.csv")
 