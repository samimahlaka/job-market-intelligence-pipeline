import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
tables = [
    "raw_linkedin_job_postings",
    "raw_job_summary",
    "raw_job_skills"
]
df = pd.read_sql("")

