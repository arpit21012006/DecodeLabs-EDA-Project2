
from pathlib import Path
import pandas as pd


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset directory
DATA_DIR = BASE_DIR / "data"


def load_dataset(file_name="Dataset for Data Analytics.xlsx"):
    """
    Load an Excel dataset and return a pandas DataFrame.
    """

    file_path = DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}\n"
            "Please place the Excel file inside the data folder."
        )

    try:
        df = pd.read_excel(file_path)

        if df.empty:
            raise ValueError("The dataset is empty.")

        print("\n" + "=" * 55)
        print("        DECODELABS PROJECT 2 - EDA")
        print("=" * 55)

        print("\n[OK] Dataset loaded successfully!")

        print(f"\nTotal Rows    : {df.shape[0]}")
        print(f"Total Columns : {df.shape[1]}")

        print("\nColumn Names:")
        for index, column in enumerate(df.columns, start=1):
            print(f"{index}. {column}")

        print("\nData Types:")
        print(df.dtypes.to_string())

        print("\nMissing Values:")
        print(df.isnull().sum().to_string())

        print("\nFirst 5 Records:")
        print(df.head().to_string(index=False))

        return df

    except Exception as error:
        print(f"\n[ERROR] Unable to load dataset: {error}")
        raise


if __name__ == "__main__":
    load_dataset()
