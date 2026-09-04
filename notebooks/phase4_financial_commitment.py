"""
Phase 4 — Financial Commitment vs Engagement Analysis
Customer Engagement & Product Utilization Analytics for Retention Strategy
"""
 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
 
SEGMENTED_PATH = "data/segmented_churn.csv"
AT_RISK_PATH = "data/at_risk_premium_customers.csv"
BALANCE_ACTIVITY_HEATMAP = "outputs/phase4_heatmap_balance_activity.png"
RATIO_CHART_PATH = "outputs/phase4_balance_salary_ratio_churn.png"
 
df = pd.read_csv(SEGMENTED_PATH)
overall_churn = df["Exited"].mean() * 100
 
# ---------------------------------------------------------------
# 1. Balance quartiles x IsActiveMember heatmap
# ---------------------------------------------------------------
print("=" * 70)
print("1. BALANCE QUARTILE x ISACTIVEMEMBER — CHURN RATE HEATMAP")
print("=" * 70)
# Note: 36.2% of customers have Balance=0 (see Phase 1), so the raw quartile edges collapse
# (Q1 and Q2 boundaries both land on 0.0). To keep four equal-sized groups, we rank Balance first
# (breaking ties by original row order) and qcut the ranks. This means "Q1 (Lowest)" is the lowest
# 25% of accounts by balance, which is mostly (but not exclusively) the zero-balance population.
n_zero_balance = (df["Balance"] == 0).sum()
print(f"Note: {n_zero_balance} customers ({n_zero_balance/len(df)*100:.1f}%) have Balance=0, which")
print("collapses standard quartile edges. Using rank-based quartiles instead (equal group sizes,")
print("ties broken arbitrarily) so all four bins remain populated.\n")
df["BalanceQuartile"] = pd.qcut(
    df["Balance"].rank(method="first"), 4,
    labels=["Q1 (Lowest)", "Q2", "Q3", "Q4 (Highest)"]
)
 
balance_activity_pivot = df.pivot_table(
    index="BalanceQuartile", columns="IsActiveMember", values="Exited",
    aggfunc="mean", observed=True
) * 100
balance_activity_pivot.columns = ["Inactive (0)", "Active (1)"]
print(balance_activity_pivot.round(1))
 
count_pivot = df.pivot_table(
    index="BalanceQuartile", columns="IsActiveMember", values="Exited",
    aggfunc="size", observed=True
)
count_pivot.columns = ["Inactive (0)", "Active (1)"]
print("\nCell counts:")
print(count_pivot)
 
fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(balance_activity_pivot, annot=True, fmt=".1f", cmap="Reds", ax=ax,
            cbar_kws={"label": "Churn Rate (%)"})
ax.set_title("Churn Rate (%): Balance Quartile x Activity Status")
plt.tight_layout()
plt.savefig(BALANCE_ACTIVITY_HEATMAP, dpi=150)
plt.close()
print(f"\nHeatmap saved to: {BALANCE_ACTIVITY_HEATMAP}")
 
# ---------------------------------------------------------------
# 2. BalanceSalaryRatio — extreme values vs churn
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("2. BALANCE-SALARY RATIO ANALYSIS")
print("=" * 70)
df["BalanceSalaryRatio"] = df["Balance"] / df["EstimatedSalary"]
 
p5 = df["BalanceSalaryRatio"].quantile(0.05)
p95 = df["BalanceSalaryRatio"].quantile(0.95)
print(f"5th percentile of BalanceSalaryRatio: {p5:.3f}")
print(f"95th percentile of BalanceSalaryRatio: {p95:.3f}")
 
df["RatioGroup"] = "Middle (5th-95th pct)"
df.loc[df["BalanceSalaryRatio"] <= p5, "RatioGroup"] = "Bottom 5% (extreme low)"
df.loc[df["BalanceSalaryRatio"] >= p95, "RatioGroup"] = "Top 5% (extreme high)"
 
ratio_churn = df.groupby("RatioGroup").agg(
    Count=("Exited", "size"),
    ChurnRate=("Exited", "mean")
)
ratio_churn["ChurnRate"] = (ratio_churn["ChurnRate"] * 100).round(2)
ratio_churn = ratio_churn.reindex(["Bottom 5% (extreme low)", "Middle (5th-95th pct)", "Top 5% (extreme high)"])
print(ratio_churn)
print(f"\n(Reference — overall churn rate: {overall_churn:.2f}%)")
 
fig, ax = plt.subplots(figsize=(8, 6))
colors = ["#c0392b" if v > overall_churn else "#2980b9" for v in ratio_churn["ChurnRate"].values]
bars = ax.bar(ratio_churn.index, ratio_churn["ChurnRate"].values, color=colors)
ax.axhline(overall_churn, color="gray", linestyle="--", linewidth=1,
           label=f"Overall churn rate ({overall_churn:.1f}%)")
for bar, val, cnt in zip(bars, ratio_churn["ChurnRate"].values, ratio_churn["Count"].values):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.5, f"{val:.1f}%\n(n={cnt})",
            ha="center", va="bottom", fontsize=9)
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Balance-to-Salary Ratio Extremity")
ax.set_xticklabels(ratio_churn.index, rotation=10, ha="right")
ax.legend()
plt.tight_layout()
plt.savefig(RATIO_CHART_PATH, dpi=150)
plt.close()
print(f"\nChart saved to: {RATIO_CHART_PATH}")
 
# ---------------------------------------------------------------
# 3. At-risk premium customers: Balance top 25% AND IsActiveMember=0
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("3. AT-RISK PREMIUM CUSTOMERS (Balance top 25% AND Inactive)")
print("=" * 70)
balance_p75 = df["Balance"].quantile(0.75)
print(f"75th percentile of Balance: {balance_p75:,.2f}")
 
at_risk = df[(df["Balance"] >= balance_p75) & (df["IsActiveMember"] == 0)].copy()
 
at_risk_count = len(at_risk)
at_risk_pct_of_customers = at_risk_count / len(df) * 100
print(f"\nCount: {at_risk_count}")
print(f"% of total customers: {at_risk_pct_of_customers:.2f}%")
 
at_risk_total_balance = at_risk["Balance"].sum()
total_bank_balance = df["Balance"].sum()
at_risk_pct_of_deposits = at_risk_total_balance / total_bank_balance * 100
print(f"\nTotal balance held by this group: {at_risk_total_balance:,.2f}")
print(f"Total balance across all customers: {total_bank_balance:,.2f}")
print(f"% of total bank deposits held by at-risk premium group: {at_risk_pct_of_deposits:.2f}%")
 
at_risk_churn = at_risk["Exited"].mean() * 100
print(f"\nChurn rate — at-risk premium group: {at_risk_churn:.2f}%")
print(f"Churn rate — overall: {overall_churn:.2f}%")
print(f"Difference: {at_risk_churn - overall_churn:+.2f} percentage points")
 
# ---------------------------------------------------------------
# 4. Save at-risk segment
# ---------------------------------------------------------------
at_risk.to_csv(AT_RISK_PATH, index=False)
print("\n" + "=" * 70)
print("4. SAVED AT-RISK PREMIUM CUSTOMER SEGMENT")
print("=" * 70)
print(f"Saved to: {AT_RISK_PATH}")
print(f"Shape: {at_risk.shape}")
 