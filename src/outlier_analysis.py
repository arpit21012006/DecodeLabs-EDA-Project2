
from pathlib import Path
import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"


def analyze_outliers(df):
    """
    Detect numerical outliers using the IQR method.
    Generate a detailed Excel report.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 55)
    print("             OUTLIER ANALYSIS")
    print("=" * 55)

    numeric_df = df.select_dtypes(include=np.number)

    summary = []
    outlier_records = []

    for column in numeric_df.columns:
        series = numeric_df[column].dropna()

        if series.empty or series.nunique() < 2:
            continue

        # Skip likely identifier columns
        if "id" in column.lower():
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_mask = (
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        )

        outlier_count = int(outlier_mask.sum())

        summary.append({
            "Column": column,
            "Q1": round(q1, 2),
            "Q3": round(q3, 2),
            "IQR": round(iqr, 2),
            "Lower_Bound": round(lower_bound, 2),
            "Upper_Bound": round(upper_bound, 2),
            "Outlier_Count": outlier_count,
            "Outlier_Percentage": round(
                outlier_count / len(df) * 100, 2
            )
        })

        if outlier_count > 0:
            for index, value in df.loc[
                outlier_mask, column
            ].items():
                outlier_records.append({
                    "Row_Index": index,
                    "Column": column,
                    "Value": value,
                    "Lower_Bound": lower_bound,
                    "Upper_Bound": upper_bound
                })

    summary_df = pd.DataFrame(
        summary,
        columns=[
            "Column", "Q1", "Q3", "IQR",
            "Lower_Bound", "Upper_Bound",
            "Outlier_Count", "Outlier_Percentage"
        ]
    )

    details_df = pd.DataFrame(
        outlier_records,
        columns=[
            "Row_Index", "Column", "Value",
            "Lower_Bound", "Upper_Bound"
        ]
    )

    output_path = REPORTS_DIR / "outlier_analysis.xlsx"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        summary_df.to_excel(
            writer, sheet_name="Outlier Summary", index=False
        )
        details_df.to_excel(
            writer, sheet_name="Outlier Details", index=False
        )

    print("\nOutlier Summary:")
    if summary_df.empty:
        print("No eligible numeric columns found.")
    else:
        print(summary_df.to_string(index=False))

    print(f"\nTotal Outlier Values: {len(details_df)}")
    print("\n[OK] Outlier analysis completed!")
    print(f"[OK] Report saved: {output_path}")

    return {
        "summary": summary_df,
        "details": details_df
    }


if __name__ == "__main__":
    from load_data import load_dataset

    dataset = load_dataset()
    analyze_outliers(dataset)

