"""
Phase 8 — Research Paper (PDF)
Customer Engagement & Product Utilization Analytics for Retention Strategy
"""
 
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle,
    ListFlowable, ListItem, KeepTogether
)
 
OUT_PATH = "report/research_paper.pdf"
CHART_DIR = "outputs"
 
# ---------------------------------------------------------------
# Styles
# ---------------------------------------------------------------
styles = getSampleStyleSheet()
 
styles.add(ParagraphStyle(
    name="PaperTitle", parent=styles["Title"], fontSize=20, leading=26,
    spaceAfter=6, textColor=colors.HexColor("#1a2530")
))
styles.add(ParagraphStyle(
    name="Subtitle", parent=styles["Normal"], fontSize=13, leading=17,
    alignment=TA_CENTER, textColor=colors.HexColor("#4a4a4a"), spaceAfter=4
))
styles.add(ParagraphStyle(
    name="MetaCenter", parent=styles["Normal"], fontSize=10, leading=14,
    alignment=TA_CENTER, textColor=colors.HexColor("#6a6a6a")
))
styles.add(ParagraphStyle(
    name="H1", parent=styles["Heading1"], fontSize=15, leading=19,
    spaceBefore=18, spaceAfter=8, textColor=colors.HexColor("#1a2530"),
    borderWidth=0, borderColor=colors.HexColor("#2980b9"),
))
styles.add(ParagraphStyle(
    name="H2", parent=styles["Heading2"], fontSize=12.5, leading=16,
    spaceBefore=12, spaceAfter=6, textColor=colors.HexColor("#2980b9")
))
styles.add(ParagraphStyle(
    name="Body", parent=styles["Normal"], fontSize=10.3, leading=15,
    alignment=TA_JUSTIFY, spaceAfter=8
))
styles.add(ParagraphStyle(
    name="Caption", parent=styles["Normal"], fontSize=8.8, leading=12,
    alignment=TA_CENTER, textColor=colors.HexColor("#5a5a5a"),
    spaceAfter=14, spaceBefore=2, fontName="Helvetica-Oblique"
))
styles.add(ParagraphStyle(
    name="BulletBody", parent=styles["Normal"], fontSize=10.3, leading=14.5,
))
 
body = styles["Body"]
h1 = styles["H1"]
h2 = styles["H2"]
caption = styles["Caption"]
 
 
def chart(filename, width=5.6):
    """Helper to embed a chart image, centered, scaled to width (inches)."""
    img = Image(f"{CHART_DIR}/{filename}", width=width * inch, height=width * inch * 0.68)
    img.hAlign = "CENTER"
    return img
 
 
def styled_table(data, col_widths=None, header=True):
    t = Table(data, colWidths=col_widths, hAlign="CENTER")
    style = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2530")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
    t.setStyle(TableStyle(style))
    return t
 
 
# ---------------------------------------------------------------
# Document
# ---------------------------------------------------------------
doc = SimpleDocTemplate(
    OUT_PATH, pagesize=letter,
    topMargin=0.85 * inch, bottomMargin=0.75 * inch,
    leftMargin=0.85 * inch, rightMargin=0.85 * inch,
)
 
story = []
 
# ---------------- Title Page ----------------
story.append(Spacer(1, 1.6 * inch))
story.append(Paragraph("Customer Engagement &amp; Product Utilization Analytics", styles["PaperTitle"]))
story.append(Paragraph("for Retention Strategy", styles["PaperTitle"]))
story.append(Spacer(1, 0.25 * inch))
story.append(Paragraph(
    "A Behavioral Analysis of Banking Customer Churn: Why Engagement and Product Depth "
    "Predict Retention Better Than Balance or Salary Alone", styles["Subtitle"]))
story.append(Spacer(1, 0.6 * inch))
story.append(Paragraph("Prepared for: Unified Mentor &nbsp;|&nbsp; The European Central Bank", styles["MetaCenter"]))
story.append(Paragraph("Dataset: European_Bank.csv &mdash; 10,000 customer records", styles["MetaCenter"]))
story.append(Paragraph("Research Paper &mdash; Internship Project Deliverable", styles["MetaCenter"]))
story.append(PageBreak())
 
# ---------------- 1. Abstract ----------------
story.append(Paragraph("1. Abstract", h1))
story.append(Paragraph(
    "Banks often assume that financially strong customers &mdash; those with high balances or "
    "salaries &mdash; are inherently loyal, yet churn frequently occurs regardless of financial "
    "standing. This study analyzes 10,000 retail banking customers to test whether behavioral "
    "engagement and product utilization predict retention better than demographic or financial "
    "attributes alone. Customers were segmented into four engagement profiles, and five KPIs were "
    "developed to quantify engagement-driven retention risk. Key findings show that active, "
    "multi-product customers churn at 9.7%, compared to 27.1% among inactive customers &mdash; a "
    "2.8x gap. Product count shows a U-shaped, not linear, relationship with churn: two products "
    "is the stickiest tier (7.6% churn), while three to four products carries near-total churn "
    "(82.7%&ndash;100%). A further 1,247 customers (12.5% of the base) hold 24.3% of total deposits "
    "while disengaged, representing concentrated financial exposure. A Random Forest model "
    "corroborates these findings while surfacing customer age as an unmodeled predictive factor. "
    "The results support engagement-first retention strategy over demographic-based targeting.",
    body
))
 
# ---------------- 2. Background & Problem Statement ----------------
story.append(Paragraph("2. Background &amp; Problem Statement", h1))
story.append(Paragraph(
    "Banks increasingly recognize that customer behavior and engagement &mdash; not just "
    "demographics &mdash; determine long-term retention. Customers may appear financially strong, "
    "carrying a high balance or salary, yet still churn due to low engagement, limited product "
    "adoption, or a weak overall relationship with the bank. Understanding how customers actually "
    "use banking products and services is essential to designing effective cross-sell strategies, "
    "loyalty programs, and engagement-driven retention initiatives.",
    body
))
story.append(Paragraph(
    "Despite banks routinely collecting data on customer engagement and product usage, "
    "organizations often lack quantitative insight into which specific behaviors drive retention, "
    "clarity on whether product depth genuinely reduces churn, and evidence on whether high "
    "balances alone are sufficient to ensure loyalty. As a result, retention strategies are "
    "frequently generic and misaligned with actual customer behavior. This project evaluates "
    "retention through the lens of customer behavior and relationship strength, with three core "
    "objectives: evaluating the relationship between engagement and churn, measuring the retention "
    "impact of product count and product mix, and identifying disengaged yet high-value customers "
    "who represent silent, high-exposure churn risk.",
    body
))
 
# ---------------- 3. Data & Methodology ----------------
story.append(Paragraph("3. Data &amp; Methodology", h1))
story.append(Paragraph(
    "The dataset comprises 10,000 customer records with 14 original fields, including credit "
    "score, geography (France, Germany, Spain), gender, age, tenure, account balance, number of "
    "products held, credit card ownership, activity status, estimated salary, and a binary churn "
    "indicator. No missing values or duplicate customer records were found. All binary fields "
    "(HasCrCard, IsActiveMember, Exited) validated as strictly 0/1, and NumOfProducts fell entirely "
    "within the expected 1&ndash;4 range. A Year field, constant at 2025 across all records, was "
    "dropped as it carried no analytical variance. Notably, 3,617 records (36.2%) carry a Balance "
    "of exactly zero; these were treated as genuine zero-balance accounts rather than missing data, "
    "since imputing them would misrepresent a substantively meaningful customer state. The overall "
    "churn rate across the cleaned dataset is 20.37% (2,037 of 10,000 customers), a class imbalance "
    "relevant to interpreting later statistical and model-based results.",
    body
))
 
story.append(Paragraph("3.1 Engagement Segmentation Rules", h2))
story.append(Paragraph(
    "Every customer was classified into exactly one of four engagement profiles, applied in "
    "priority order (first match wins):", body
))
seg_table_data = [
    ["Segment", "Rule"],
    ["Active Engaged", "IsActiveMember = 1 AND NumOfProducts >= 2"],
    ["Inactive Disengaged", "IsActiveMember = 0 AND NumOfProducts = 1"],
    ["Active Low-Product", "IsActiveMember = 1 AND NumOfProducts = 1"],
    ["Inactive High-Balance", "IsActiveMember = 0 AND Balance >= 75th percentile"],
]
story.append(styled_table(seg_table_data, col_widths=[1.8 * inch, 3.9 * inch]))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "1,909 customers (19.1%) were inactive, multi-product, but below the balance threshold, and "
    "so did not cleanly match any rule; these were folded into &ldquo;Inactive Disengaged&rdquo; "
    "since inactivity was judged the dominant churn signal. This is an explicit analyst judgment "
    "call, stated here for methodological transparency.",
    body
))
 
# ---------------- 4. EDA Findings ----------------
story.append(Paragraph("4. EDA Findings", h1))
 
story.append(Paragraph("4.1 Engagement Profile Findings", h2))
story.append(Paragraph(
    "Activity status proved to be the single strongest behavioral split found in the dataset. The "
    "Active Engaged segment (25.9% of customers) churns at just 9.7%, less than half the overall "
    "rate, while Inactive Disengaged customers &mdash; the largest single segment at 44.3% of the "
    "base &mdash; churn at 27.1%, nearly three times higher. The Inactive High-Balance segment "
    "(4.2% of customers) is particularly concerning: despite meaningful deposits, this group "
    "churns at 24.6%, confirming that balance alone does not buy loyalty.",
    body
))
story.append(chart("phase2_churn_by_engagement_profile.png"))
story.append(Paragraph("Figure 1. Churn rate by engagement profile, sorted highest to lowest.", caption))
 
seg_summary_data = [
    ["Segment", "Count", "% of Base", "Churn Rate"],
    ["Inactive Disengaged", "4,430", "44.3%", "27.1%"],
    ["Inactive High-Balance", "419", "4.2%", "24.6%"],
    ["Active Low-Product", "2,563", "25.6%", "18.9%"],
    ["Active Engaged", "2,588", "25.9%", "9.7%"],
]
story.append(styled_table(seg_summary_data, col_widths=[1.9 * inch, 1.0 * inch, 1.2 * inch, 1.2 * inch]))
story.append(Spacer(1, 12))
 
story.append(Paragraph("4.2 Product Utilization Findings", h2))
story.append(Paragraph(
    "Product count and churn do not move in a straight line &mdash; the relationship is U-shaped. "
    "Customers with two products are the stickiest group in the entire dataset (7.6% churn, "
    "n=4,590), while single-product customers churn nearly four times higher (27.7%, n=5,084). "
    "Beyond two products, however, churn does not continue to fall: it inverts sharply. "
    "Three-product customers churn at 82.7% and four-product customers churn at a full 100% "
    "(n=60, small group, direction still meaningful). A chi-square test comparing single- versus "
    "multi-product customers confirms high significance (chi-square = 342.98, p &lt; 0.001), though "
    "this aggregate framing masks the more important finding: two products is protective, while "
    "three to four products is the strongest churn signal found anywhere in this analysis.",
    body
))
story.append(chart("phase3_churn_by_numproducts.png"))
story.append(Paragraph("Figure 2. Churn rate by number of products held, with group sizes annotated.", caption))
 
story.append(Paragraph(
    "This pattern directly contradicts the standard &ldquo;more products = more loyalty&rdquo; "
    "assumption past a threshold of two, and it is not a regional or age-group artifact: it holds "
    "consistently across France, Germany, and Spain, and across every age band from under-30 to "
    "60+. Two plausible explanations warrant further investigation: (1) customers with three to "
    "four products may represent accounts nearing exit that were cross-sold additional products "
    "shortly before leaving, making product count a lagging symptom rather than a cause of "
    "disengagement; or (2) a servicing or origination artifact specific to three-to-four product "
    "bundles (e.g. a discontinued offer or under-supported tier) that correlates with, rather than "
    "causes, churn.",
    body
))
story.append(chart("phase3_heatmap_products_geography.png", width=4.6))
story.append(Paragraph("Figure 3. Churn rate (%) by product count and geography &mdash; the U-shape holds in every market.", caption))
story.append(chart("phase3_heatmap_products_age.png", width=4.6))
story.append(Paragraph("Figure 4. Churn rate (%) by product count and age band &mdash; the U-shape holds across every age group.", caption))
 
story.append(Paragraph("4.3 Financial Commitment vs. Engagement Findings", h2))
story.append(Paragraph(
    "At-risk premium customers &mdash; defined as customers in the top 25% of account balance who "
    "are also disengaged &mdash; number 1,247, or 12.5% of the entire customer base. This group "
    "holds $185.6 million in deposits, representing 24.3% of the bank's total balance sheet "
    "($764.9 million). In plain terms: roughly 1 in 8 customers, holding nearly a quarter of all "
    "deposits, are disengaged and at elevated churn risk. This group churns at 30.5%, exceeding "
    "the overall rate of 20.4% by more than 10 percentage points.",
    body
))
story.append(chart("phase4_heatmap_balance_activity.png", width=4.6))
story.append(Paragraph("Figure 5. Churn rate (%) by balance quartile and activity status.", caption))
story.append(Paragraph(
    "The balance-quartile breakdown reinforces this: among inactive customers, churn rises with "
    "balance (18.4% in the lowest quartile up to 34.2% in the third quartile), while active "
    "customers stay well below the overall average regardless of balance (10.5%&ndash;18.8% across "
    "all four quartiles). Balance only becomes a churn risk factor once engagement is already "
    "missing &mdash; a high-balance, active customer is not at elevated risk, but a high-balance, "
    "disengaged customer is the bank's single highest-value flight risk. A supplementary check of "
    "balance-to-salary ratio extremity did not yield additional signal beyond this quartile "
    "pattern, as the &ldquo;extreme low&rdquo; tail was distorted by the large zero-balance "
    "population rather than reflecting a genuine outlier group.",
    body
))
 
# ---------------- 5. KPI Framework & Results ----------------
story.append(Paragraph("5. KPI Framework &amp; Results", h1))
story.append(Paragraph(
    "Five KPIs were developed to translate the behavioral findings above into reusable, "
    "monitorable metrics:", body
))
 
kpi_formula_data = [
    ["KPI", "Formula"],
    ["Engagement Retention Ratio", "churn rate (inactive) / churn rate (active)"],
    ["Product Depth Index", "Pearson correlation of NumOfProducts vs. grouped churn rate"],
    ["High-Balance Disengagement Rate", "% of top-quartile-balance customers who are inactive"],
    ["Credit Card Stickiness Score", "churn rate (no card) minus churn rate (has card)"],
    ["Relationship Strength Index", "0.4 x Active + 0.3 x (Products/4) + 0.2 x (Tenure/10, capped) + 0.1 x Card"],
]
story.append(styled_table(kpi_formula_data, col_widths=[2.1 * inch, 4.3 * inch]))
story.append(Spacer(1, 10))
 
story.append(Paragraph("5.1 Results by Geography", h2))
kpi_results_data = [
    ["KPI", "Overall", "France", "Germany", "Spain"],
    ["Engagement Retention Ratio", "1.88x", "1.84x", "1.73x", "2.17x"],
    ["Product Depth Index", "+0.858", "+0.880", "+0.783", "+0.889"],
    ["High-Balance Disengagement Rate", "49.9%", "50.7%", "48.6%", "45.0%"],
    ["Credit Card Stickiness Score", "+0.63 pp", "+0.32 pp", "+0.79 pp", "+1.70 pp"],
]
story.append(styled_table(kpi_results_data, col_widths=[2.3 * inch, 1.0 * inch, 1.0 * inch, 1.05 * inch, 1.0 * inch]))
story.append(Spacer(1, 12))
 
story.append(Paragraph("5.2 KPI Validation", h2))
story.append(Paragraph(
    "Four of the five KPIs behaved as expected; one surfaced a genuine exception worth flagging "
    "explicitly rather than smoothing over. The Engagement Retention Ratio (1.88x overall) "
    "confirms inactive customers churn nearly twice as often as active ones, holding across all "
    "three markets. The Credit Card Stickiness Score is positive in all three countries, "
    "confirming card ownership is mildly protective everywhere, strongest in Spain (+1.70 pp). "
    "The Relationship Strength Index is the clearest success: churn falls monotonically across "
    "every quartile, from 28.8% in the weakest-relationship quartile down to 12.7% in the "
    "strongest &mdash; a clean validation that the composite weighting captures real retention "
    "signal.",
    body
))
story.append(chart("phase5_rsi_churn_by_quartile.png"))
story.append(Paragraph("Figure 6. Churn rate by Relationship Strength Index quartile &mdash; a clean, monotonic decline.", caption))
story.append(Paragraph(
    "The Product Depth Index is the one KPI that inverts naive expectation, by design and not by "
    "error: it was defined as the correlation between product count and grouped churn rate, which "
    "directly encodes the Section 4.2 finding. The correlation is strongly positive (+0.858 "
    "overall, positive in all three countries), meaning more products associates with higher churn "
    "across the dataset as a whole, because the index is dominated by the extreme three-to-four "
    "product cliff. This KPI should therefore be read as &ldquo;product-count risk "
    "concentration,&rdquo; not &ldquo;product depth benefit&rdquo; &mdash; a distinction worth "
    "stating explicitly so the metric is not misread at a glance. Finally, the High-Balance "
    "Disengagement Rate (49.9% overall, roughly a coin flip, consistent 45&ndash;51% across "
    "markets) reinforces that balance alone says nothing about engagement; it must be paired with "
    "activity status to identify real risk.",
    body
))
 
# ---------------- 6. Predictive Validation ----------------
story.append(Paragraph("6. Predictive Validation", h1))
story.append(Paragraph(
    "As an independent check on the KPI framework, a Random Forest classifier (200 trees, max "
    "depth 8, class-balanced weighting, 80/20 train-test split) was trained to predict churn from "
    "all available customer attributes. This was treated as supporting evidence, not a "
    "deployment-ready model.",
    body
))
model_metrics_data = [
    ["Metric", "Value"],
    ["Accuracy", "81.95%"],
    ["Precision (Exited = 1)", "54.46%"],
    ["Recall (Exited = 1)", "69.04%"],
]
story.append(styled_table(model_metrics_data, col_widths=[2.6 * inch, 1.6 * inch]))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Given the approximately 20% churn class imbalance, accuracy alone is not the meaningful "
    "number here &mdash; a model that always predicted &ldquo;stayed&rdquo; would already score "
    "roughly 80%. Precision and recall on the churned class are more informative: the model "
    "correctly flags roughly 7 in 10 actual churners, at the cost of a moderate false-positive "
    "rate, a reasonable trade-off for retention-targeting use cases where missing a churner is "
    "costlier than an unnecessary retention outreach.",
    body
))
story.append(chart("phase6_confusion_matrix.png", width=4.2))
story.append(Paragraph("Figure 7. Confusion matrix on the held-out test set (n=2,000).", caption))
story.append(chart("phase6_feature_importances.png", width=5.4))
story.append(Paragraph("Figure 8. Random Forest feature importances, ranked highest to lowest.", caption))
story.append(Paragraph(
    "The feature importances partially support and partially complicate the KPI framework. "
    "NumOfProducts ranks as the second most important feature overall (importance 0.255), directly "
    "corroborating the product-count cliff identified in Sections 4.2 and 5.2 as a dominant, "
    "data-confirmed churn driver. IsActiveMember also registers as meaningfully important (ranked "
    "4th), supporting the engagement-based KPIs. However, Age emerges as the single strongest "
    "predictor by a wide margin (importance 0.365, ahead of every engagement or product variable) "
    "&mdash; a feature not incorporated into any of the five KPIs. This is a genuine gap worth "
    "flagging: age's dominance suggests older customers may be churning for reasons the current "
    "engagement/product framework does not capture, such as retirement, life-stage banking needs, "
    "or a support experience that skews poorly for older customers. Notably, EstimatedSalary ranks "
    "low (5th), reinforcing the core project thesis that raw salary is not a meaningful churn "
    "driver on its own, in contrast to behavioral and structural variables like age and product "
    "count.",
    body
))
 
# ---------------- 7. Recommendations ----------------
story.append(Paragraph("7. Recommendations", h1))
rec_items = [
    ListItem(Paragraph(
        "<b>Prioritize re-engagement over pure cross-sell.</b> Since activity status alone moves "
        "churn risk further than adding a second or third product (9.7% vs. 27.1% churn between "
        "active and inactive segments), retention budget should favor activation nudges and usage "
        "incentives for the Inactive Disengaged segment (44.3% of the base) ahead of generic "
        "cross-sell campaigns.", styles["BulletBody"])),
    ListItem(Paragraph(
        "<b>Cap cross-sell at two products and investigate the three-to-four product cliff as a "
        "priority, not a footnote.</b> Given churn jumps from 7.6% at two products to 82.7&ndash;"
        "100% at three to four products, sales teams should stop treating additional products past "
        "two as an automatic loyalty win, and a root-cause investigation (servicing quality, "
        "bundling practices, or exit-driven cross-sell timing) should be commissioned immediately.",
        styles["BulletBody"])),
    ListItem(Paragraph(
        "<b>Launch a dedicated retention program for the 1,247 at-risk premium customers.</b> This "
        "group holds $185.6 million (24.3% of deposits) while disengaged and churning at 30.5%. "
        "Given the concentrated financial exposure, this segment justifies white-glove relationship "
        "management rather than mass-market retention tactics.", styles["BulletBody"])),
    ListItem(Paragraph(
        "<b>Adopt the Relationship Strength Index as an ongoing monitoring metric</b>, since it "
        "cleanly and monotonically predicts churn (28.8% to 12.7% across quartiles), and route "
        "the bottom quartile into proactive outreach workflows.", styles["BulletBody"])),
    ListItem(Paragraph(
        "<b>Investigate age as a retention factor</b> in a follow-up study, given it was the "
        "strongest predictor in the Random Forest model yet sits entirely outside the current KPI "
        "framework &mdash; an age-banded engagement KPI is a natural next iteration.",
        styles["BulletBody"])),
]
story.append(ListFlowable(rec_items, bulletType="bullet", start="circle", leftIndent=16, spaceBefore=4, bulletFontSize=6))
story.append(Spacer(1, 8))
 
# ---------------- 8. Limitations ----------------
story.append(Paragraph("8. Limitations", h1))
lim_items = [
    ListItem(Paragraph(
        "<b>Single-snapshot dataset.</b> The data represents one point in time (the Year field was "
        "constant), so no trend, cohort, or time-to-churn analysis was possible; findings describe "
        "association, not confirmed causal direction.", styles["BulletBody"])),
    ListItem(Paragraph(
        "<b>Analyst-defined thresholds.</b> The EngagementProfile segmentation rules and the "
        "balance quartile cutoffs used throughout are reasoned judgment calls, not universal "
        "definitions; 19.1% of customers required a fallback classification rule.",
        styles["BulletBody"])),
    ListItem(Paragraph(
        "<b>No causal mechanism confirmed for the product-count cliff.</b> The three-to-four "
        "product churn spike is a robust statistical pattern, but this analysis cannot distinguish "
        "whether products caused disengagement, were a symptom of it, or reflect an unrelated "
        "servicing issue.", styles["BulletBody"])),
    ListItem(Paragraph(
        "<b>Predictive model is illustrative, not production-ready.</b> The Random Forest model "
        "was built for KPI validation, not deployment; it was not tuned, cross-validated across "
        "multiple splits, or tested for fairness across demographic groups.", styles["BulletBody"])),
]
story.append(ListFlowable(lim_items, bulletType="bullet", start="circle", leftIndent=16, spaceBefore=4, bulletFontSize=6))
story.append(Spacer(1, 8))
 
# ---------------- 9. Conclusion ----------------
story.append(Paragraph("9. Conclusion", h1))
story.append(Paragraph(
    "This project reframes customer churn from a behavioral and relationship-strength perspective "
    "rather than a demographic one. The evidence is consistent across every analytical lens used "
    "&mdash; segmentation, cross-tabulation, KPI construction, and independent model validation "
    "&mdash; that engagement status and product-count structure predict churn far more reliably "
    "than balance or salary alone. The clearest actionable finding is that disengagement, not low "
    "wealth, is the bank's core retention problem: the highest-exposure customers are not the "
    "poorest, but the wealthiest ones who have stopped engaging. Equally important is the discovery "
    "that product depth is not uniformly protective; retention strategy must treat the two-product "
    "tier as the target state rather than assuming that more is always better. Together, these "
    "findings support a shift from generic, demographic-led retention campaigns toward "
    "engagement-driven, exposure-weighted interventions &mdash; with age flagged as a priority "
    "area for future research beyond the scope of the current KPI framework.",
    body
))
 
# ---------------- Build ----------------
doc.build(story)
print(f"PDF built: {OUT_PATH}")
 