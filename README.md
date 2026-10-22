## Simple ETL Pipeline — Retail Transaction Dataset
Proyek ini adalah pipeline ETL (Extract, Transform, Load) sederhana untuk mengambil data transaksi retail dari Kaggle, membersihkannya menggunakan Python/Pandas, memasukkannya ke dalam database PostgreSQL, dan melakukan verifikasi kualitas data menggunakan SQL.

## Arsitektur Pipeline
1. Extract: Mengunduh dataset Retail Transaction Dataset (100.000 baris) dari Kaggle API.
2. Transform: Membersihkan data dengan Pandas (konversi tipe tanggal, cek duplikat, validasi anomali).
3. Load: Memuat data bersih ke tabel retail_transactions di PostgreSQL.
4. Quality Check: Menjalankan query SQL untuk membuktikan data 100% valid.

## Dataset
Dataset yang digunakan: [Retail Transaction Dataset](https://www.kaggle.com/datasets/fahadrehman07/retail-transaction-dataset)
Memiliki 10 kolom, termasuk: CustomerID, ProductID, Quantity, Price, TransactionDate, PaymentMethod, StoreLocation, ProductCategory, DiscountApplied(%), dan TotalAmount.

Cara Menjalankan Proyek
1. Prasyarat
Python 3.10+
PostgreSQL 14+ (berjalan di localhost)
Akun Kaggle & file kaggle.json

2. Setup Environment
bash
git clone
cd retail
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Unduh Data
Letakkan kaggle.json di direktori ~/.kaggle/ (Mac/Linux) atau C:\Users\<user>\.kaggle\ (Windows), lalu jalankan:
bash
kaggle datasets download -d fahadrehman07/retail-transaction-dataset -p ./data --unzip

4. Konfigurasi Database
Buat database di PostgreSQL

5. Jalankan ETL
bash
python scripts/transform.py
python scripts/load.py
Keputusan Pembersihan Data (Transform)
Konversi Tipe Tanggal: Kolom TransactionDate awalnya bertipe string. Saya mengonversinya menjadi tipe datetime menggunakan pd.to_datetime(errors='coerce').
Deduplikasi: Menghapus baris yang sepenuhnya identik menggunakan drop_duplicates().
Validasi Logika: Memeriksa apakah ada Quantity <= 0, Price <= 0, atau TotalAmount negatif.
Konsistensi Total: Memastikan TotalAmount sesuai dengan rumus Quantity × Price × (1 - Discount/100).

## Hasil Verifikasi Kualitas Data (Quality Check)
Setelah data dimuat ke PostgreSQL, saya menjalankan query SQL untuk memastikan tidak ada data yang corrupt atau dirty.
https://docs/query_results.png

Ringkasan Hasil:
Total baris: 100.000 baris berhasil dimuat.
Tanggal NULL: 0 (konversi berhasil 100%).
Quantity/Price tidak wajar: 0.
TotalAmount negatif: 0.
TotalAmount mismatch rumus: 0.
Duplikat: 0.

## Keterbatasan & Perbaikan Selanjutnya
- Saat ini skrip menggunakan if_exists='replace'. Di lingkungan produksi, sebaiknya menggunakan append dengan mekanisme idempotensi (seperti ON CONFLICT) untuk mencegah duplikasi data jika skrip dijalankan berulang kali.
- Belum ada scheduling (cron/Airflow). Bisa ditambahkan untuk menjalankan pipeline secara otomatis setiap hari.