import pandas as pd
import os

RAW_PATH = "data/raw/Retail_Transaction_Dataset.csv"
PROCESSED_PATH = "data/processed.csv"


def load_raw(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File tidak ditemukan: {path}. Jalankan download Kaggle dulu.")
    df = pd.read_csv(path)
    print(f"[LOAD] Baris awal: {len(df)}, Kolom: {list(df.columns)}")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Konversi TransactionDate dari string ke datetime
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"], errors="coerce")
    na_dates = df["TransactionDate"].isna().sum()
    print(f"[TRANSFORM] Baris dengan tanggal gagal dikonversi (NaT): {na_dates}")

    # 2. Hapus duplikat penuh
    before = len(df)
    df = df.drop_duplicates()
    print(f"[TRANSFORM] Baris duplikat dihapus: {before - len(df)}")

    # 3. Validasi logika: Quantity & Price harus > 0
    invalid_qty = (df["Quantity"] <= 0).sum()
    invalid_price = (df["Price"] <= 0).sum()
    print(f"[TRANSFORM] Quantity <= 0: {invalid_qty}, Price <= 0: {invalid_price}")

    # 4. Validasi TotalAmount tidak negatif
    invalid_total = (df["TotalAmount"] < 0).sum()
    print(f"[TRANSFORM] TotalAmount negatif: {invalid_total}")

    # 5. Cek konsistensi TotalAmount vs Quantity * Price * (1 - Discount/100)
    expected = df["Quantity"] * df["Price"] * (1 - df["DiscountApplied(%)"] / 100)
    mismatch = (abs(expected - df["TotalAmount"]) > 0.01).sum()
    print(f"[TRANSFORM] Baris dengan TotalAmount tidak sesuai rumus: {mismatch}")

    # 6. Hapus baris dengan tanggal NaT (opsional, sesuaikan kebijakan Anda)
    df = df.dropna(subset=["TransactionDate"])

    print(f"[TRANSFORM] Baris akhir setelah transform: {len(df)}")
    return df


def main():
    df = load_raw(RAW_PATH)
    df_clean = transform(df)
    df_clean.to_csv(PROCESSED_PATH, index=False)
    print(f"[SAVE] Data bersih disimpan ke {PROCESSED_PATH}")


if __name__ == "__main__":
    main()