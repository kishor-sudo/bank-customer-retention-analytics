"""
Phase 3 — Product Utilization Analysis
Customer Engagement & Product Utilization Analytics for Retention Strategy
"""
 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
 
SEGMENTED_PATH = "data/segmented_churn.csv"
BAR_CHART_PATH = "outputs/phase3_churn_by_numproducts.png"
GEO_HEATMAP_PATH = "outputs/phase3_heatmap_products_geography.png"
AGE_HEATMAP_PATH = "outputs/phase3_heatmap_products_age.png"
 
df = pd.read_csv(SEGMENTED_PATH)
 
# ---------------------------------------------------------------
# 1. Churn rate grouped by NumOfProducts, with counts
# ---------------------------------------------------------------
print("=" * 70)
print("1. CHURN RATE BY NUMOFPRODUCTS")
print("=" * 70)
grouped = df.groupby("NumOfProducts").agg(
    Count=("Exited", "size"),
    ChurnRate=("Exited", "mean")
)
grouped["ChurnRate"] = (grouped["ChurnRate"] * 100).round(2)
grouped["PctOfCustomers"] = (grouped["Count"] / len(df) * 100).round(1)
print(grouped)
 
small_groups = grouped[grouped["Count"] < 200]
if len(small_groups) > 0:
    print(f"\nNote: small group(s) with <200 customers — interpret with caution:")
    print(small_groups)
 
# ---------------------------------------------------------------
# 2. Chi-square test: single-product vs multi-product churn
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("2. CHI-SQUARE TEST — SINGLE VS MULTI-PRODUCT CHURN")
print("=" * 70)
df["ProductGroup"] = np.where(df["NumOfProducts"] == 1, "Single-Product", "Multi-Product")
contingency = pd.crosstab(df["ProductGroup"], df["Exited"])
print("Contingency table:")
print(contingency)
 
chi2, p_value, dof, expected = chi2_contingency(contingency)
print(f"\nChi-square statistic: {chi2:.4f}")
print(f"p-value: {p_value:.6f}")
print(f"Degrees of freedom: {dof}")
alpha = 0.05
significant = p_value < alpha
print(f"Significant at alpha=0.05: {significant}")
 
single_churn = df.loc[df["ProductGroup"] == "Single-Product", "Exited"].mean() * 100
multi_churn = df.loc[df["ProductGroup"] == "Multi-Product", "Exited"].mean() * 100
print(f"\nSingle-product churn rate: {single_churn:.2f}%")
print(f"Multi-product churn rate: {multi_churn:.2f}%")
 
# ---------------------------------------------------------------
# 3. Bar chart — churn rate vs NumOfProducts
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6))
churn_by_prod = grouped["ChurnRate"]
overall_churn = df["Exited"].mean() * 100
colors = ["#c0392b" if v > overall_churn else "#2980b9" for v in churn_by_prod.values]
bars = ax.bar(churn_by_prod.index.astype(str), churn_by_prod.values, color=colors)
ax.axhline(overall_churn, color="gray", linestyle="--", linewidth=1,
           label=f"Overall churn rate ({overall_churn:.1f}%)")
for bar, val, cnt in zip(bars, churn_by_prod.values, grouped["Count"].values):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.5, f"{val:.1f}%\n(n={cnt})",
            ha="center", va="bottom", fontsize=9)
ax.set_xlabel("Number of Products")
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Number of Products")
ax.legend()
plt.tight_layout()
plt.savefig(BAR_CHART_PATH, dpi=150)
plt.close()
print(f"\nChart saved to: {BAR_CHART_PATH}")
 
# ---------------------------------------------------------------
# 4. Cross-tab heatmaps: NumOfProducts x Geography, NumOfProducts x Age band
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("4. CROSS-TAB: NUMOFPRODUCTS x GEOGRAPHY")
print("=" * 70)
geo_pivot = df.pivot_table(index="NumOfProducts", columns="Geography",
                             values="Exited", aggfunc="mean") * 100
print(geo_pivot.round(1))
 
fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(geo_pivot, annot=True, fmt=".1f", cmap="Reds", ax=ax,
            cbar_kws={"label": "Churn Rate (%)"})
ax.set_title("Churn Rate (%): NumOfProducts x Geography")
plt.tight_layout()
plt.savefig(GEO_HEATMAP_PATH, dpi=150)
plt.close()
print(f"Heatmap saved to: {GEO_HEATMAP_PATH}")
 
print("\n" + "=" * 70)
print("4b. CROSS-TAB: NUMOFPRODUCTS x AGE BAND")
print("=" * 70)
bins = [0, 30, 45, 60, 150]
labels = ["<30", "30-45", "45-60", "60+"]
df["AgeBand"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)
 
age_pivot = df.pivot_table(index="NumOfProducts", columns="AgeBand",
                             values="Exited", aggfunc="mean", observed=True) * 100
print(age_pivot.round(1))
 
age_count_pivot = df.pivot_table(index="NumOfProducts", columns="AgeBand",
                                   values="Exited", aggfunc="size", observed=True)
print("\nCell counts (for context — small cells are noisy):")
print(age_count_pivot)
 
fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(age_pivot, annot=True, fmt=".1f", cmap="Reds", ax=ax,
            cbar_kws={"label": "Churn Rate (%)"})
ax.set_title("Churn Rate (%): NumOfProducts x Age Band")
plt.tight_layout()
plt.savefig(AGE_HEATMAP_PATH, dpi=150)
plt.close()
print(f"Heatmap saved to: {AGE_HEATMAP_PATH}")
 
# ---------------------------------------------------------------
# 5. Explicit check: do 3-4 product customers churn MORE than 1-2?
# ---------------------------------------------------------------
print("\n" + "=" * 70)
print("5. PRODUCT-COUNT PARADOX CHECK")
print("=" * 70)
low_group_churn = df.loc[df["NumOfProducts"].isin([1, 2]), "Exited"].mean() * 100
high_group_churn = df.loc[df["NumOfProducts"].isin([3, 4]), "Exited"].mean() * 100
print(f"Churn rate, 1-2 products: {low_group_churn:.2f}%")
print(f"Churn rate, 3-4 products: {high_group_churn:.2f}%")
 
paradox_found = high_group_churn > low_group_churn
print(f"\nParadox present (3-4 products churn MORE than 1-2): {paradox_found}")
 
if paradox_found:
    print("\nFLAG: This contradicts the standard 'more products = more loyalty' assumption.")
    print("Possible explanations to investigate further:")
    print("  1. Customers with 3-4 products may have been aggressively cross-sold products")
    print("     they don't actually use/need, creating friction rather than stickiness")
    print("     (products acquired without matching engagement/need).")
    print("  2. 3-4 product customers may be a small, unusual subgroup (check group size)")
    print("     possibly concentrated in a specific acquisition channel or bundled offer")
    print("     that has its own unrelated churn driver (e.g. a promo that later disappoints).")
 