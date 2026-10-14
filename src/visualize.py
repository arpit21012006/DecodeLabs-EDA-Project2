
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "visualizations"

# Professional warm neutral theme
BG = "#FAF8F5"
PRIMARY = "#806D5D"
SECONDARY = "#B59D87"
ACCENT = "#D7BFA9"

sns.set_theme(style="whitegrid", font_scale=1.0)


def save_chart(filename):
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / filename,
        dpi=220,
        bbox_inches="tight",
        facecolor=BG
    )
    plt.close()
    print(f"[OK] Chart saved: {filename}")


def generate_visualizations(df):
    """
    Generate professional EDA visualizations.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 55)
    print("           EDA DATA VISUALIZATIONS")
    print("=" * 55)

    # Prepare data without changing original dataset
    data = df.copy()

    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(
            data["Date"], errors="coerce"
        )

    for col in ["TotalPrice", "Quantity", "UnitPrice"]:
        if col in data.columns:
            data[col] = pd.to_numeric(
                data[col], errors="coerce"
            )

    # 1. Monthly Sales Trend
    if {"Date", "TotalPrice"}.issubset(data.columns):
        sales = data.dropna(
            subset=["Date", "TotalPrice"]
        ).copy()

        sales["Month"] = sales["Date"].dt.to_period("M")

        monthly = (
            sales.groupby("Month")["TotalPrice"]
            .sum()
            .sort_index()
        )

        if not monthly.empty:
            plt.figure(figsize=(11, 5.5))
            plt.plot(
                monthly.index.astype(str),
                monthly.values,
                marker="o",
                linewidth=2.5,
                color=PRIMARY
            )
            plt.title(
                "Monthly Sales Trend",
                fontsize=16,
                fontweight="bold"
            )
            plt.xlabel("Month")
            plt.ylabel("Total Sales")
            plt.xticks(rotation=45, ha="right")
            save_chart("01_monthly_sales_trend.png")

    # 2. Top Products by Revenue
    if {"Product", "TotalPrice"}.issubset(data.columns):
        top_products = (
            data.groupby("Product")["TotalPrice"]
            .sum()
            .nlargest(10)
            .sort_values()
        )

        if not top_products.empty:
            plt.figure(figsize=(10, 6))
            plt.barh(
                top_products.index.astype(str),
                top_products.values,
                color=SECONDARY
            )
            plt.title(
                "Top 10 Products by Revenue",
                fontsize=16,
                fontweight="bold"
            )
            plt.xlabel("Total Sales")
            plt.ylabel("Product")
            save_chart("02_top_products.png")

    # 3. Payment Method Distribution
    if "PaymentMethod" in data.columns:
        payments = (
            data["PaymentMethod"]
            .fillna("Unknown")
            .value_counts()
        )

        if not payments.empty:
            plt.figure(figsize=(9, 5.5))
            sns.barplot(
                x=payments.values,
                y=payments.index.astype(str),
                color=PRIMARY
            )
            plt.title(
                "Payment Method Distribution",
                fontsize=16,
                fontweight="bold"
            )
            plt.xlabel("Number of Orders")
            plt.ylabel("Payment Method")
            save_chart("03_payment_methods.png")

    # 4. Order Status Distribution
    if "OrderStatus" in data.columns:
        statuses = (
            data["OrderStatus"]
            .fillna("Unknown")
            .value_counts()
        )

        if not statuses.empty:
            plt.figure(figsize=(9, 5.5))
            sns.barplot(
                x=statuses.values,
                y=statuses.index.astype(str),
                color=SECONDARY
            )
            plt.title(
                "Order Status Distribution",
                fontsize=16,
                fontweight="bold"
            )
            plt.xlabel("Number of Orders")
            plt.ylabel("Order Status")
            save_chart("04_order_status.png")

    # 5. Total Price Distribution
    if "TotalPrice" in data.columns:
        values = data["TotalPrice"].dropna()

        if not values.empty:
            plt.figure(figsize=(10, 5.5))
            sns.histplot(
                values,
                bins=30,
                kde=True,
                color=PRIMARY
            )
            plt.title(
                "Order Value Distribution",
                fontsize=16,
                fontweight="bold"
            )
            plt.xlabel("Total Price")
            plt.ylabel("Frequency")
            save_chart("05_price_distribution.png")

    # 6. Correlation Heatmap
    numeric = data.select_dtypes(
        include=np.number
    ).copy()

    # Exclude identifiers from correlation
    numeric = numeric.drop(
        columns=[
            c for c in numeric.columns
            if "id" in c.lower()
        ],
        errors="ignore"
    )

    numeric = numeric.loc[
        :,
        numeric.nunique(dropna=True) > 1
    ]

    if numeric.shape[1] >= 2:
        correlation = numeric.corr()

        plt.figure(figsize=(9, 7))
        sns.heatmap(
            correlation,
            annot=True,
            fmt=".2f",
            cmap="BrBG",
            center=0,
            linewidths=0.5,
            square=True
        )
        plt.title(
            "Numerical Feature Correlation",
            fontsize=16,
            fontweight="bold"
        )
        save_chart("06_correlation_heatmap.png")

    print("\n[OK] Visualization generation completed!")
    print(f"[OK] Charts directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    from load_data import load_dataset

    dataset = load_dataset()
    generate_visualizations(dataset)
