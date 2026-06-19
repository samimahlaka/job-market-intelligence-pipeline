import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv


def main():
    load_dotenv()

    dataset = os.getenv("KAGGLE_DATASET")
    raw_data_dir = os.getenv("RAW_DATA_DIR", "data/raw")

    if not dataset:
        raise ValueError("KAGGLE_DATASET is missing. Add it to your .env file.")

    output_path = Path(raw_data_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    command = [
        "kaggle",
        "datasets",
        "download",
        "-d",
        dataset,
        "-p",
        str(output_path),
        "--unzip",
    ]

    print(f"Downloading dataset: {dataset}")
    print(f"Saving to: {output_path}")

    subprocess.run(command, check=True)

    print("Dataset downloaded successfully.")


if __name__ == "__main__":
    main()