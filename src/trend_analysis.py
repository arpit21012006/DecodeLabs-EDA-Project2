
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"


def analyze_trends(df):
    """
    Analyze monthly sales, product performance,
    payment methods, and order statuses.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 55)
    print("                TREND ANALYSIS")
    print("=" * 55)

    results = {}

    # 1. Monthly Sales Analysis
    if {"Date", "TotalPrice"}.issubset(df.columns):
        sales_df = df.copy()

        sales_df["Date"] = pd.to_datetime(
            sales_df["Date"], errors="coerce"
        )

        sales_df["TotalPrice"] = pd.to_numeric(
            sales_df["TotalPrice"], errors="coerce"
        )

        sales_df = sales_df.dropna(
            subset=["Date", "TotalPrice"]
        )

        sales_df["Month"] = (
            sales_df["Date"].dt.to_period("M").astype(str)
        )

        monthly_sales = (
            sales_df.groupby("Month")["TotalPrice"]
            .agg(["sum", "mean", "count"])
            .reset_index()
            .sort_values("Month")
        )

        monthly_sales.columns = [
            "Month",
            "Total_Sales",
            "Average_Order_Value",
            "Order_Count"
        ]

        results["Monthly Sales"] = monthly_sales

    # 2. Product Performance
    if {"Product", "TotalPrice"}.issubset(df.columns):
        product_df = df.copy()

        product_df["TotalPrice"] = pd.to_numeric(
            product_df["TotalPrice"], errors="coerce"
        )

        product_performance = (
            product_df.groupby("Product", dropna=False)["TotalPrice"]
            .agg(["sum", "mean", "count"])
            .reset_index()
            .sort_values("sum", ascending=False)
        )

        product_performance.columns = [
            "Product",
            "Total_Sales",
            "Average_Order_Value",
            "Order_Count"
        ]

        results["Product Performance"] = product_performance

    # 3. Payment Method Distribution
    if "PaymentMethod" in df.columns:
        payment_distribution = (
            df["PaymentMethod"]
            .value_counts(dropna=False)
            .rename_axis("Payment_Method")
            .reset_index(name="Order_Count")
        )

        results["Payment Methods"] = payment_distribution

    # 4. Order Status Distribution
    if "OrderStatus" in df.columns:
        status_distribution = (
            df["OrderStatus"]
            .value_counts(dropna=False)
            .rename_axis("Order_Status")
            .reset_index(name="Order_Count")
        )

        results["Order Status"] = status_distribution

    # Export Results
    output_path = REPORTS_DIR / "trend_analysis.xlsx"

    if not results:
        print("\n[WARNING] No matching columns found.")
        return results

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, result_df in results.items():
            result_df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False
            )

    # Display Results
    for name, result_df in results.items():
        print(f"\n{name}:")
        print(result_df.to_string(index=False))

    print("\n[OK] Trend analysis completed!")
    print(f"[OK] Report saved: {output_path}")

    return results


if __name__ == "__main__":
    from load_data import load_dataset

    dataset = load_dataset()
    analyze_trends(dataset)
