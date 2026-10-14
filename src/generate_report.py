
from pathlib import Path
import pandas as pd
import numpy as np

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image, PageBreak,
    KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from xml.sax.saxutils import escape


BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
CHART_DIR = BASE_DIR / "visualizations"


def generate_report(df):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = REPORT_DIR / "EDA_Final_Report.pdf"

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=(595.28, 841.89),
        rightMargin=42,
        leftMargin=42,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontSize=21,
        leading=27,
        textColor=colors.HexColor("#51463D"),
        spaceAfter=18
    ))

    styles.add(ParagraphStyle(
        name="SectionTitleCustom",
        parent=styles["Heading2"],
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#806D5D"),
        spaceBefore=14,
        spaceAfter=9
    ))

    styles.add(ParagraphStyle(
        name="BodyCustom",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=15,
        spaceAfter=9
    ))

    story = []

    def heading(text):
        story.append(
            Paragraph(text, styles["SectionTitleCustom"])
        )

    def body(text):
        story.append(
            Paragraph(escape(str(text)), styles["BodyCustom"])
        )

    def add_table(rows):
        formatted = [
            [str(value) for value in row]
            for row in rows
        ]

        table = Table(
            formatted,
            repeatRows=1,
            hAlign="LEFT"
        )

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#806D5D")),
            ("TEXTCOLOR", (0, 0), (-1, 0),
             colors.white),
            ("FONTNAME", (0, 0), (-1, 0),
             "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 9),
            ("TOPPADDING", (0, 0), (-1, 0), 9),
            ("GRID", (0, 0), (-1, -1),
             0.35, colors.HexColor("#DDDDDD")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#F5F1ED")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
        ]))

        story.append(table)
        story.append(Spacer(1, 12))

    def add_chart(filename, caption):
        path = CHART_DIR / filename

        if not path.exists():
            body(f"Chart unavailable: {filename}")
            return

        width, height = ImageReader(str(path)).getSize()
        max_width = 495
        max_height = 335
        scale = min(
            max_width / width,
            max_height / height
        )

        img = Image(
            str(path),
            width=width * scale,
            height=height * scale
        )

        story.append(KeepTogether([
            img,
            Spacer(1, 6),
            Paragraph(
                escape(caption),
                styles["BodyCustom"]
            )
        ]))

    # Title
    story.append(Paragraph(
        "EXPLORATORY DATA ANALYSIS",
        styles["ReportTitle"]
    ))

    body("Project 2 | DecodeLabs Data Analytics Internship")
    body("Dataset: Dataset for Data Analytics.xlsx")

    heading("1. Project Objective")

    body(
        "This project explores an order transaction dataset "
        "using descriptive statistics, trend analysis, "
        "outlier detection, and data visualization. "
        "The objective is to identify patterns and summarize "
        "observations supported by the available data."
    )

    heading("2. Dataset Overview")

    rows, cols = df.shape
    missing = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())

    add_table([
        ["Metric", "Value"],
        ["Total Records", rows],
        ["Total Columns", cols],
        ["Missing Values", missing],
        ["Duplicate Rows", duplicates]
    ])

    heading("3. Descriptive Statistics")

    numeric = df.select_dtypes(include=np.number)

    if not numeric.empty:
        stats_rows = [
            ["Feature", "Mean", "Median", "Min", "Max"]
        ]

        for col in numeric.columns:
            if "id" in col.lower():
                continue

            series = numeric[col].dropna()

            if series.empty:
                continue

            stats_rows.append([
                col[:22],
                f"{series.mean():,.2f}",
                f"{series.median():,.2f}",
                f"{series.min():,.2f}",
                f"{series.max():,.2f}"
            ])

        if len(stats_rows) > 1:
            add_table(stats_rows)

    heading("4. Sales and Product Insights")

    data = df.copy()

    if "TotalPrice" in data.columns:
        data["TotalPrice"] = pd.to_numeric(
            data["TotalPrice"], errors="coerce"
        )

        total_sales = data["TotalPrice"].sum()
        avg_order = data["TotalPrice"].mean()

        body(f"Total recorded sales value: {total_sales:,.2f}")
        body(f"Average recorded order value: {avg_order:,.2f}")

    if {"Product", "TotalPrice"}.issubset(data.columns):
        product_sales = (
            data.groupby("Product")["TotalPrice"]
            .sum()
            .sort_values(ascending=False)
        )

        if not product_sales.empty:
            body(
                "Highest revenue product: "
                f"{product_sales.index[0]} "
                f"({product_sales.iloc[0]:,.2f})"
            )

    if {"Date", "TotalPrice"}.issubset(data.columns):
        data["Date"] = pd.to_datetime(
            data["Date"], errors="coerce"
        )

        valid = data.dropna(
            subset=["Date", "TotalPrice"]
        ).copy()

        if not valid.empty:
            monthly = (
                valid.groupby(
                    valid["Date"].dt.to_period("M")
                )["TotalPrice"]
                .sum()
                .sort_index()
            )

            if not monthly.empty:
                body(
                    "Highest sales month: "
                    f"{monthly.idxmax()} "
                    f"({monthly.max():,.2f})"
                )

                body(
                    "Lowest sales month: "
                    f"{monthly.idxmin()} "
                    f"({monthly.min():,.2f})"
                )

    heading("5. Customer Order Patterns")

    for column, label in [
        ("PaymentMethod", "Most common payment method"),
        ("OrderStatus", "Most common order status"),
        ("ReferralSource", "Most common referral source")
    ]:
        if column in data.columns:
            counts = data[column].dropna().value_counts()

            if not counts.empty:
                body(
                    f"{label}: {counts.index[0]} "
                    f"({counts.iloc[0]} records)"
                )

    heading("6. Outlier Analysis")

    for column in numeric.columns:
        if "id" in column.lower():
            continue

        values = numeric[column].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        count = int(
            ((values < lower) | (values > upper)).sum()
        )

        body(
            f"{column}: {count} potential outliers "
            "identified using the IQR method."
        )

    body(
        "Potential outliers should be investigated before "
        "being removed. An unusual value is not necessarily "
        "an incorrect value."
    )

    story.append(PageBreak())

    heading("7. Data Visualizations")

    charts = [
        ("01_monthly_sales_trend.png",
         "Figure 1: Monthly Sales Trend"),
        ("02_top_products.png",
         "Figure 2: Top Products by Revenue"),
        ("03_payment_methods.png",
         "Figure 3: Payment Method Distribution"),
        ("04_order_status.png",
         "Figure 4: Order Status Distribution"),
        ("05_price_distribution.png",
         "Figure 5: Order Value Distribution"),
        ("06_correlation_heatmap.png",
         "Figure 6: Numerical Feature Correlation")
    ]

    for filename, caption in charts:
        add_chart(filename, caption)

    heading("8. Conclusion")

    body(
        "The exploratory analysis summarizes transaction "
        "values, product performance, order patterns, "
        "monthly trends, and potential numerical outliers. "
        "The charts and statistical reports provide a "
        "foundation for further business analysis. "
        "These findings describe observed patterns and "
        "do not establish causal relationships."
    )

    doc.build(story)

    print(f"[OK] Final PDF report generated: {output_path}")


if __name__ == "__main__":
    from load_data import load_dataset

    dataset = load_dataset()
    generate_report(dataset)
