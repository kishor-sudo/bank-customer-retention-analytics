"""
Streamlit Dashboard — Customer Engagement & Product Utilization Analytics for Retention Strategy
Phase 7 deliverable.
 
Run with: streamlit run app/main.py
"""
 
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 
st.set_page_config(page_title="Retention Analytics Dashboard", layout="wide")
 
DATA_WITH_RSI = "data/segmented_churn_with_rsi.csv"
DATA_SEGMENTED = "data/segmented_churn.csv"
KPI_SUMMARY_PATH = "outputs/kpi_summary.csv"
 
 
# ---------------------------------------------------------------
# Cached data loading
# ---------------------------------------------------------------
@st.cache_data
def load_data():
    """Load the segmented customer dataset, computing RelationshipStrengthIndex if needed."""
    if os.path.exists(DATA_WITH_RSI):
        df = pd.read_csv(DATA_WITH_RSI)
    else:
        df = pd.read_csv(DATA_SEGMENTED)
        from src.kpis import relationship_strength_index
        df["RelationshipStrengthIndex"] = relationship_strength_index(df)
    return df
 
 
@st.cache_data
def load_kpi_summary():
    if os.path.exists(KPI_SUMMARY_PATH):
        return pd.read_csv(KPI_SUMMARY_PATH)
    return None
 
 
df = load_data()
kpi_df = load_kpi_summary()
overall_churn = df["Exited"].mean() * 100
 
 
def get_kpi_value(kpi_name, breakdown="Overall"):
    """Pull a single KPI value out of the kpi_summary table, if available."""
    if kpi_df is None:
        return None
    match = kpi_df[(kpi_df["KPI"] == kpi_name) & (kpi_df["Breakdown"] == breakdown)]
    if len(match) == 0:
        return None
    return match["Value"].iloc[0]
 
 
# ---------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------
st.sidebar.title("Retention Analytics")
page = st.sidebar.radio(
    "Choose a module",
    [
        "1. Engagement vs Churn Overview",
        "2. Product Utilization Impact",
        "3. High-Value Disengaged Detector",
        "4. Retention Strength Scoring",
    ],
)
 
st.sidebar.markdown("---")
st.sidebar.caption(f"Dataset: {len(df):,} customers | Overall churn rate: {overall_churn:.1f}%")
 
 
# =================================================================
# MODULE 1 — Engagement vs Churn Overview
# =================================================================
if page.startswith("1"):
    st.title("Engagement vs Churn Overview")
 
    err_val = get_kpi_value("Engagement Retention Ratio")
    hbdr_val = get_kpi_value("High-Balance Disengagement Rate (%)")
    ccss_val = get_kpi_value("Credit Card Stickiness Score (pp)")
 
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Overall Churn Rate", f"{overall_churn:.1f}%")
    col2.metric("Engagement Retention Ratio", f"{err_val:.2f}x" if err_val is not None else "N/A",
                help="Inactive customer churn rate ÷ active customer churn rate")
    col3.metric("High-Balance Disengagement Rate", f"{hbdr_val:.1f}%" if hbdr_val is not None else "N/A",
                help="% of top-quartile-balance customers who are inactive")
    col4.metric("Credit Card Stickiness", f"{ccss_val:+.2f} pp" if ccss_val is not None else "N/A",
                help="Churn rate (no card) minus churn rate (has card)")
 
    st.markdown("### Churn Rate by Engagement Profile")
    churn_by_segment = df.groupby("EngagementProfile")["Exited"].mean().mul(100).sort_values(ascending=False)
 
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = ["#c0392b" if v > overall_churn else "#2980b9" for v in churn_by_segment.values]
    bars = ax.bar(churn_by_segment.index, churn_by_segment.values, color=colors)
    ax.axhline(overall_churn, color="gray", linestyle="--", linewidth=1,
               label=f"Overall churn rate ({overall_churn:.1f}%)")
    for bar, val in zip(bars, churn_by_segment.values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.5, f"{val:.1f}%",
                ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Churn Rate (%)")
    ax.legend()
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
 
    highest = churn_by_segment.idxmax()
    lowest = churn_by_segment.idxmin()
    st.caption(
        f"💡 **{highest}** customers churn nearly {churn_by_segment.max()/churn_by_segment.min():.1f}x "
        f"more often than **{lowest}** customers — engagement, not balance, drives retention."
    )
 
 
# =================================================================
# MODULE 2 — Product Utilization Impact
# =================================================================
elif page.startswith("2"):
    st.title("Product Utilization Impact")
 
    prod_range = st.slider("Filter by number of products", min_value=1, max_value=4, value=(1, 4))
 
    grouped = df.groupby("NumOfProducts").agg(Count=("Exited", "size"), ChurnRate=("Exited", "mean"))
    grouped["ChurnRate"] = grouped["ChurnRate"] * 100
 
    fig, ax = plt.subplots(figsize=(8, 4.5))
    in_range = [(prod_range[0] <= idx <= prod_range[1]) for idx in grouped.index]
    colors = [
        ("#c0392b" if v > overall_churn else "#2980b9") if sel else "#d5d8dc"
        for v, sel in zip(grouped["ChurnRate"].values, in_range)
    ]
    bars = ax.bar(grouped.index.astype(str), grouped["ChurnRate"].values, color=colors)
    ax.axhline(overall_churn, color="gray", linestyle="--", linewidth=1,
               label=f"Overall churn rate ({overall_churn:.1f}%)")
    for bar, val, cnt in zip(bars, grouped["ChurnRate"].values, grouped["Count"].values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 1, f"{val:.1f}%\n(n={cnt})",
                ha="center", va="bottom", fontsize=9)
    ax.set_xlabel("Number of Products")
    ax.set_ylabel("Churn Rate (%)")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
 
    st.caption(
        "💡 Churn is U-shaped, not linear: 2 products is the stickiest tier, but 3-4 products "
        "carries dramatically higher churn — more products does not automatically mean more loyalty."
    )
 
    st.markdown(f"### Customers with {prod_range[0]}–{prod_range[1]} products")
    filtered = df[df["NumOfProducts"].between(prod_range[0], prod_range[1])]
    st.write(f"Showing {len(filtered):,} customers (churn rate in this range: {filtered['Exited'].mean()*100:.1f}%)")
    st.dataframe(
        filtered[["CustomerId", "Geography", "Age", "NumOfProducts", "Balance",
                  "IsActiveMember", "EngagementProfile", "Exited"]].reset_index(drop=True),
        use_container_width=True,
        height=350,
    )
 
 
# =================================================================
# MODULE 3 — High-Value Disengaged Customer Detector
# =================================================================
elif page.startswith("3"):
    st.title("High-Value Disengaged Customer Detector")
    st.write("Reproduce the 'at-risk premium customers' segment interactively, or adjust the thresholds.")
 
    col1, col2, col3 = st.columns(3)
    min_balance = col1.slider("Minimum Balance", 0, int(df["Balance"].max()),
                               int(df["Balance"].quantile(0.75)), step=5000)
    min_salary = col2.slider("Minimum Estimated Salary", 0, int(df["EstimatedSalary"].max()), 0, step=5000)
    inactive_only = col3.checkbox("Inactive members only", value=True)
 
    filtered = df[(df["Balance"] >= min_balance) & (df["EstimatedSalary"] >= min_salary)]
    if inactive_only:
        filtered = filtered[filtered["IsActiveMember"] == 0]
 
    pct_of_customers = len(filtered) / len(df) * 100
    pct_of_deposits = filtered["Balance"].sum() / df["Balance"].sum() * 100 if df["Balance"].sum() > 0 else 0
    churn_rate = filtered["Exited"].mean() * 100 if len(filtered) > 0 else 0
 
    col1, col2, col3 = st.columns(3)
    col1.metric("Customers matched", f"{len(filtered):,}", f"{pct_of_customers:.1f}% of base")
    col2.metric("Deposits held", f"${filtered['Balance'].sum():,.0f}", f"{pct_of_deposits:.1f}% of total")
    col3.metric("Churn rate (this group)", f"{churn_rate:.1f}%",
                f"{churn_rate - overall_churn:+.1f} pp vs overall")
 
    st.caption(
        "💡 A small slice of high-balance, disengaged customers can hold a disproportionate share "
        "of total deposits — that concentration is the real business exposure, not just headcount."
    )
 
    st.markdown("### Matching customers")
    st.dataframe(
        filtered[["CustomerId", "Geography", "Age", "Balance", "EstimatedSalary",
                  "IsActiveMember", "NumOfProducts", "EngagementProfile", "Exited"]]
        .sort_values("Balance", ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=400,
    )
 
 
# =================================================================
# MODULE 4 — Retention Strength Scoring
# =================================================================
elif page.startswith("4"):
    st.title("Retention Strength Scoring")
 
    rsi_min, rsi_max = float(df["RelationshipStrengthIndex"].min()), float(df["RelationshipStrengthIndex"].max())
    score_range = st.slider("Filter by Relationship Strength Index range",
                             min_value=round(rsi_min, 2), max_value=round(rsi_max, 2),
                             value=(round(rsi_min, 2), round(rsi_max, 2)), step=0.01)
 
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(df["RelationshipStrengthIndex"], bins=30, color="#d5d8dc", edgecolor="white")
    in_range = df[df["RelationshipStrengthIndex"].between(score_range[0], score_range[1])]
    ax.hist(in_range["RelationshipStrengthIndex"], bins=30, color="#2980b9", edgecolor="white",
            range=(rsi_min, rsi_max))
    ax.set_xlabel("Relationship Strength Index (0-1)")
    ax.set_ylabel("Number of Customers")
    ax.set_title("Distribution of Relationship Strength Index")
    plt.tight_layout()
    st.pyplot(fig)
 
    filtered_churn = in_range["Exited"].mean() * 100 if len(in_range) > 0 else 0
    col1, col2 = st.columns(2)
    col1.metric("Customers in selected range", f"{len(in_range):,}")
    col2.metric("Churn rate in this range", f"{filtered_churn:.1f}%",
                f"{filtered_churn - overall_churn:+.1f} pp vs overall")
 
    st.caption(
        "💡 Churn falls steadily as the Relationship Strength Index rises — the weakest-relationship "
        "quartile churns over twice as often as the strongest, confirming the index tracks real risk."
    )
 