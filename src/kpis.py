"""
src/kpis.py — Reusable KPI functions
Customer Engagement & Product Utilization Analytics for Retention Strategy
 
Each function takes a DataFrame (expects columns: IsActiveMember, NumOfProducts, Balance,
HasCrCard, Tenure, Exited) and returns a KPI value (or Series for per-customer KPIs).
"""
 
import pandas as pd
import numpy as np
 
 
def engagement_retention_ratio(df: pd.DataFrame) -> float:
    """
    Engagement Retention Ratio = churn_rate(inactive) / churn_rate(active)
 
    >1 means inactive customers churn more than active customers (expected direction).
    """
    churn_inactive = df.loc[df["IsActiveMember"] == 0, "Exited"].mean()
    churn_active = df.loc[df["IsActiveMember"] == 1, "Exited"].mean()
    if churn_active == 0:
        return np.nan
    return churn_inactive / churn_active
 
 
def product_depth_index(df: pd.DataFrame) -> float:
    """
    Product Depth Index = Pearson correlation between NumOfProducts and churn rate,
    computed on the GROUPED (product-count-level) churn rate, not row-level.
 
    Positive => more products associates with higher churn.
    Negative => more products associates with lower churn (the "expected" direction
    under a naive "more products = more loyalty" assumption).
    """
    grouped = df.groupby("NumOfProducts")["Exited"].mean().reset_index()
    if grouped["NumOfProducts"].nunique() < 2:
        return np.nan
    return grouped["NumOfProducts"].corr(grouped["Exited"])
 
 
def high_balance_disengagement_rate(df: pd.DataFrame, balance_col: str = "Balance") -> float:
    """
    High-Balance Disengagement Rate = % of top-quartile-balance customers who are inactive.
    """
    p75 = df[balance_col].quantile(0.75)
    top_quartile = df[df[balance_col] >= p75]
    if len(top_quartile) == 0:
        return np.nan
    return (top_quartile["IsActiveMember"] == 0).mean() * 100
 
 
def credit_card_stickiness_score(df: pd.DataFrame) -> float:
    """
    Credit Card Stickiness Score = churn_rate(no card) - churn_rate(has card)
 
    Positive => having a card is associated with LOWER churn (cards are "sticky", expected direction).
    Negative => having a card is associated with HIGHER churn (unexpected).
    """
    churn_no_card = df.loc[df["HasCrCard"] == 0, "Exited"].mean()
    churn_has_card = df.loc[df["HasCrCard"] == 1, "Exited"].mean()
    return (churn_no_card - churn_has_card) * 100
 
 
def relationship_strength_index(df: pd.DataFrame) -> pd.Series:
    """
    Relationship Strength Index (per customer, 0-1 scale):
        0.4 * IsActiveMember
      + 0.3 * (NumOfProducts / 4)
      + 0.2 * min(Tenure / 10, 1)
      + 0.1 * HasCrCard
 
    Higher = stronger relationship. Should correlate with LOWER churn if the weighting is sound.
    """
    tenure_component = (df["Tenure"] / 10).clip(upper=1)
    score = (
        0.4 * df["IsActiveMember"]
        + 0.3 * (df["NumOfProducts"] / 4)
        + 0.2 * tenure_component
        + 0.1 * df["HasCrCard"]
    )
    return score
 