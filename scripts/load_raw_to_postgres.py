from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")

engine = create_engine(DATABASE_URL)

RAW_DATA_DIR = Path("data/raw")
CHUNK_SIZE = 50_000


def clean_table_name(file_path: Path) -> str:
    return "raw_" + file_path.stem.lower().replace("-", "_").replace(" ", "_")


def load_csv_to_postgres(csv_path: Path):
    table_name = clean_table_name(csv_path)

    print(f"\nLoading {csv_path.name} into table: {table_name}")

    first_chunk = True
    total_rows = 0

    for chunk in pd.read_csv(csv_path, chunksize=CHUNK_SIZE, low_memory=False):
        chunk.to_sql(
            table_name,
            engine,
            if_exists="replace" if first_chunk else "append",
            index=False,
            method="multi",
        )

        total_rows += len(chunk)
        first_chunk = False
        print(f"Loaded {total_rows:,} rows into {table_name}")

    print(f"Finished {table_name}: {total_rows:,} rows")


def main():
    csv_files = list(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found in data/raw")
        return

    for csv_file in csv_files:
        load_csv_to_postgres(csv_file)

    print("\nAll raw CSV files loaded into PostgreSQL.")


if __name__ == "__main__":
    main()