
from src.load_data import load_dataset
from src.descriptive_stats import analyze_statistics
from src.outlier_analysis import analyze_outliers
from src.trend_analysis import analyze_trends
from src.visualize import generate_visualizations
from src.generate_report import generate_report


def main():
    print("=" * 60)
    print("       DECODELABS - EDA PROJECT 2")
    print("=" * 60)

    print("\n[1/6] Loading dataset...")
    df = load_dataset()

    print("\n[2/6] Descriptive statistics...")
    analyze_statistics(df)

    print("\n[3/6] Outlier analysis...")
    analyze_outliers(df)

    print("\n[4/6] Trend analysis...")
    analyze_trends(df)

    print("\n[5/6] Generating visualizations...")
    generate_visualizations(df)

    print("\n[6/6] Generating final PDF report...")
    generate_report(df)

    print("\n" + "=" * 60)
    print("PROJECT 2 COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()
