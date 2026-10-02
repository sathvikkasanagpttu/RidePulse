import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "cleaned_data.csv"
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured. Copy .env.example to .env and add your PostgreSQL connection string.")

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
df.to_sql("trips", engine, if_exists="replace", index=False)
print(f"Loaded {len(df):,} rows into the 'trips' table.")
