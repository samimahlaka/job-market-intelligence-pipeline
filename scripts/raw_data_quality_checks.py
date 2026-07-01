import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

tables = [
    "raw_linkedin_job_postings",
    "raw_job_summary",
    "raw_job_skills",
]

def run_query(query):
    with engine.connect() as conn:
        return conn.execute(text(query)).fetchone()[0]

def check_table_counts():
    print("\nROW COUNTS")
    print("=" * 50)

    for table in tables:
        count = run_query(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {count:,} rows")

def check_null_job_links():
    print("\nNULL JOB_LINK CHECK")
    print("=" * 50)

    for table in tables:
        null_count = run_query(f"SELECT COUNT(*) FROM {table} WHERE job_link IS NULL")
        print(f"{table}: {null_count:,} null job_link values")

def check_duplicate_job_links():
    print("\nDUPLICATE JOB_LINK CHECK")
    print("=" * 50)

    for table in tables:
        duplicate_count = run_query(f"""
            SELECT COUNT(*)
            FROM (
                SELECT job_link
                FROM {table}
                GROUP BY job_link
                HAVING COUNT(*) > 1
            ) duplicates
        """)
        print(f"{table}: {duplicate_count:,} duplicate job_link values")

def main():
    check_table_counts()
    check_null_job_links()
    check_duplicate_job_links()

    print("\nRaw data quality checks completed.")

if __name__ == "__main__":  