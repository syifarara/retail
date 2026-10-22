import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

PROCESSED_PATH = "data/processed/processed.csv"
TABLE_NAME = "retail_transactions"


def main():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL tidak ditemukan di .env")

    if not os.path.exists(PROCESSED_PATH):
        raise FileNotFoundError(f"{PROCESSED_PATH} tidak ada. Jalankan transform.py dulu.")

    df = pd.read_csv(PROCESSED_PATH, parse_dates=["TransactionDate"])
    print(f"[LOAD] Baris yang akan dimuat: {len(df)}")

    engine = create_engine(db_url)
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
    print(f"[LOAD] Berhasil memuat {len(df)} baris ke tabel '{TABLE_NAME}'")


if __name__ == "__main__":
    main()