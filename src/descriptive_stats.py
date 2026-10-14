
from pathlib import Path
import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"


def analyze_statistics(df):
    """
    Perform descriptive statistical analysis and
    export the results to an Excel workbook.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 55)
    print("       DESCRIPTIVE STATISTICAL ANALYSIS")
    print("=" * 55)

    # Dataset overview
    overview = pd.DataFrame({
        "Metric": [
            "Total Rows",
            "Total Columns",
            "Total Missing Values",
            "Duplicate Rows",
            "Numeric Columns",
            "Categorical Columns"
        ],
        "Value": [
            len(df),
            len(df.columns),
            int(df.isna().sum().sum()),
            int(df.duplicated().sum()),
            len(df.select_dtypes(include=np.number).columns),
            len(df.select_dtypes(exclude=np.number).columns)
        ]
    })

    # Numeric descriptive statistics
    numeric_df = df.select_dtypes(include=np.number)

    if not numeric_df.empty:
        numeric_stats = numeric_df.describe().T.reset_index()
        numeric_stats.rename(
            columns={"index": "Column"},
            inplace=True
        )
        numeric_stats["median"] = numeric_df.median().values
        numeric_stats["missing"] = numeric_df.isna().sum().values
    else:
        numeric_stats = pd.DataFrame({
            "Message": ["No numeric columns found"]
        })

    # Categorical descriptive statistics
    categorical_df = df.select_dtypes(exclude=np.number)

    if not categorical_df.empty:
        categorical_stats = categorical_df.describe().T.reset_index()
        categorical_stats.rename(
            columns={"index": "Column"},
            inplace=True
        )
    else:
        categorical_stats = pd.DataFrame({
            "Message": ["No categorical columns found"]
        })

    # Missing value summary
    missing_summary = pd.DataFrame({
        "Column": df.columns,
        "Missing_Count": df.isna().sum().values,
        "Missing_Percentage": (
            df.isna().mean().values * 100
        ).round(2)
    })

    # Export Excel report
    output_path = REPORTS_DIR / "descriptive_statistics.xlsx"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        overview.to_excel(
            writer, sheet_name="Dataset Overview", index=False
        )
        numeric_stats.to_excel(
            writer, sheet_name="Numeric Statistics", index=False
        )
        categorical_stats.to_excel(
            writer, sheet_name="Categorical Statistics", index=False
        )
        missing_summary.to_excel(
            writer, sheet_name="Missing Values", index=False
        )

    print("\nDataset Overview:")
    print(overview.to_string(index=False))

    print("\nNumeric Statistics:")
    print(numeric_stats.to_string(index=False))

    print("\n[OK] Statistical analysis completed!")
    print(f"[OK] Report saved: {output_path}")

    return {
        "overview": overview,
        "numeric_stats": numeric_stats,
        "categorical_stats": categorical_stats,
        "missing_summary": missing_summary
    }


if __name__ == "__main__":
    from load_data import load_dataset

    dataset = load_dataset()
    analyze_statistics(dataset)
