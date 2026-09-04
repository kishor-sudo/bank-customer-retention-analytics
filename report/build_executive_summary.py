"""
Phase 9 — Executive Summary (PDF, 1 page)
Customer Engagement & Product Utilization Analytics for Retention Strategy
"""
 
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
)
 
OUT_PATH = "report/executive_summary.pdf"
 
styles = getSampleStyleSheet()
 
styles.add(ParagraphStyle(
    name="ExecTitle", parent=styles["Title"], fontSize=17, leading=21,
    textColor=colors.HexColor("#1a2530"), spaceAfter=2
))
styles.add(ParagraphStyle(
    name="ExecSubtitle", parent=styles["Normal"], fontSize=9.5, leading=13,
    textColor=colors.HexColor("#6a6a6a"), spaceAfter=10
))
styles.add(ParagraphStyle(
    name="SectionLabel", parent=styles["Normal"], fontSize=9, leading=11,
    textColor=colors.HexColor("#2980b9"), fontName="Helvetica-Bold",
    spaceBefore=10, spaceAfter=4
))
styles.add(ParagraphStyle(
    name="CoreFinding", parent=styles["Normal"], fontSize=12.5, leading=17,
    textColor=colors.HexColor("#1a2530"), fontName="Helvetica-Bold",
    alignment=TA_LEFT
))
styles.add(ParagraphStyle(
    name="StatNumber", parent=styles["Normal"], fontSize=22, leading=24,
    textColor=colors.HexColor("#1a2530"), fontName="Helvetica-Bold",
    alignment=TA_CENTER, spaceAfter=2
))
styles.add(ParagraphStyle(
    name="StatLabel", parent=styles["Normal"], fontSize=8.7, leading=11.5,
    textColor=colors.HexColor("#3a3a3a"), alignment=TA_CENTER
))
styles.add(ParagraphStyle(
    name="BodySmall", parent=styles["Normal"], fontSize=9.8, leading=13.5,
    alignment=TA_JUSTIFY
))
styles.add(ParagraphStyle(
    name="RecBody", parent=styles["Normal"], fontSize=9.8, leading=13.5,
))
styles.add(ParagraphStyle(
    name="Footer", parent=styles["Normal"], fontSize=7.8, leading=10,
    textColor=colors.HexColor("#8a8a8a"), alignment=TA_CENTER
))
 
doc = SimpleDocTemplate(
    OUT_PATH, pagesize=letter,
    topMargin=0.55 * inch, bottomMargin=0.5 * inch,
    leftMargin=0.65 * inch, rightMargin=0.65 * inch,
)
 
story = []
 
# ---------------- Header ----------------
story.append(Paragraph("Customer Retention: Executive Summary", styles["ExecTitle"]))
story.append(Paragraph(
    "Customer Engagement &amp; Product Utilization Analytics for Retention Strategy &nbsp;|&nbsp; "
    "Prepared for policy and executive stakeholders &nbsp;|&nbsp; Based on 10,000 customer records",
    styles["ExecSubtitle"]
))
 
# ---------------- Core Finding ----------------
core_finding_table = Table(
    [[Paragraph(
        "Customer engagement &mdash; not account balance or salary &mdash; is the strongest, "
        "most consistent predictor of whether a customer leaves the bank.",
        styles["CoreFinding"]
    )]],
    colWidths=[7.1 * inch]
)
core_finding_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eaf2f8")),
    ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#2980b9")),
    ("LEFTPADDING", (0, 0), (-1, -1), 14),
    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
]))
story.append(core_finding_table)
story.append(Spacer(1, 12))
 
# ---------------- Headline Numbers ----------------
story.append(Paragraph("THE NUMBERS THAT MATTER", styles["SectionLabel"]))
 
def stat_cell(number, label):
    return [Paragraph(number, styles["StatNumber"]), Paragraph(label, styles["StatLabel"])]
 
stat_data = [[
    stat_cell("9.7% vs 27.1%", "Churn rate for engaged customers vs. disengaged customers &mdash; nearly 3x higher risk when engagement is lost"),
    stat_cell("24.3% of deposits", "Held by disengaged customers who make up just 12.5% of customers &mdash; $185.6M concentrated in a flight-risk group"),
    stat_cell("82&ndash;100% churn", "Among customers holding 3&ndash;4 products &mdash; more products does not automatically mean more loyalty"),
]]
 
# Wrap each cell's two paragraphs into a mini-table so they stack inside one grid cell
def stat_box(number, label):
    inner = Table([[Paragraph(number, styles["StatNumber"])], [Paragraph(label, styles["StatLabel"])]],
                   colWidths=[2.25 * inch])
    inner.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return inner
 
stats_row = [
    stat_box("9.7% vs 27.1%", "Churn rate: engaged vs. disengaged customers &mdash; nearly 3x higher risk when engagement is lost"),
    stat_box("24.3% of deposits", "Held by the 12.5% of customers who are disengaged &mdash; $185.6M concentrated in a flight-risk group"),
    stat_box("82&ndash;100% churn", "Among customers holding 3&ndash;4 products &mdash; more products does not automatically mean more loyalty"),
]
stats_table = Table([stats_row], colWidths=[2.37 * inch, 2.37 * inch, 2.37 * inch])
stats_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7f9fa")),
    ("BOX", (0, 0), (0, 0), 0.75, colors.HexColor("#d0d5d8")),
    ("BOX", (1, 0), (1, 0), 0.75, colors.HexColor("#d0d5d8")),
    ("BOX", (2, 0), (2, 0), 0.75, colors.HexColor("#d0d5d8")),
    ("TOPPADDING", (0, 0), (-1, -1), 12),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(stats_table)
story.append(Spacer(1, 6))
 
# ---------------- What this means ----------------
story.append(Paragraph("WHAT THIS MEANS", styles["SectionLabel"]))
story.append(Paragraph(
    "The bank's biggest retention risk is not poor or low-value customers &mdash; it is wealthy, "
    "disengaged ones. A customer who stops using the bank actively is far more likely to leave "
    "than one who simply holds a lower balance. At the same time, encouraging customers to hold "
    "more products is not a reliable loyalty strategy on its own: customers with two products are "
    "the most loyal group in the bank, but customers pushed to three or four products leave at "
    "extremely high rates. Retention efforts built around balance, salary, or product count alone "
    "will miss the customers most likely to leave &mdash; and misdirect resources toward customers "
    "who were never at risk.",
    styles["BodySmall"]
))
 
# ---------------- Recommendations ----------------
story.append(Paragraph("RECOMMENDED ACTIONS", styles["SectionLabel"]))
rec_items = [
    ListItem(Paragraph(
        "<b>Redirect retention spend toward re-engagement, not just cross-selling.</b> "
        "Reactivating disengaged customers will reduce churn more than offering them additional "
        "products.", styles["RecBody"])),
    ListItem(Paragraph(
        "<b>Create a dedicated outreach program for high-value disengaged customers.</b> "
        "Roughly 1,250 customers hold nearly a quarter of all deposits while disengaged &mdash; "
        "protecting this group should be a top priority, not a routine campaign.",
        styles["RecBody"])),
    ListItem(Paragraph(
        "<b>Pause further product-bundling expansion beyond two products until the cause of the "
        "3&ndash;4 product churn spike is understood.</b> Investigate whether this reflects "
        "aggressive sales practices, poor servicing, or customers already planning to leave.",
        styles["RecBody"])),
]
story.append(ListFlowable(rec_items, bulletType="bullet", start="circle", leftIndent=14,
                           spaceBefore=2, bulletFontSize=6))
 
story.append(Spacer(1, 10))
story.append(Paragraph(
    "Full methodology, statistical testing, and supporting charts are available in the "
    "accompanying research paper.", styles["Footer"]
))
 
doc.build(story)
print(f"PDF built: {OUT_PATH}")
 