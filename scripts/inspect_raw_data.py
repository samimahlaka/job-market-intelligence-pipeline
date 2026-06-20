from pathlib import Path

import pandas as pd


RAW_DATA_DIR = Path("data/raw")


def inspect_csv_files():
    for file in RAW_DATA_DIR.glob("*.csv"):
        print("\n" + "=" * 80)
        print(f"File: {file}")

        df = pd.read_csv(file, nrows=5)

        print(f"Sample shape: {df.shape}")
        print("Columns:")
        print(df.columns.tolist())

        print("\nPreview:")
        print(df.head())


if __name__ == "__main__":
    inspect_csv_files()