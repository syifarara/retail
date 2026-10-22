-- 1. Total baris (harus sama dengan jumlah baris processed.csv)
SELECT COUNT(*) AS total_rows FROM retail_transactions;

-- 2. Cek apakah ada TransactionDate yang NULL (gagal konversi)
SELECT COUNT(*) AS null_dates
FROM retail_transactions
WHERE "TransactionDate" IS NULL;

-- 3. Cek duplikat berdasarkan kombinasi CustomerID + ProductID + TransactionDate
SELECT "CustomerID", "ProductID", "TransactionDate", COUNT(*) AS cnt
FROM retail_transactions
GROUP BY "CustomerID", "ProductID", "TransactionDate"
HAVING COUNT(*) > 1
ORDER BY cnt DESC
LIMIT 10;

-- 4. Cek Quantity atau Price yang tidak wajar
SELECT COUNT(*) AS invalid_quantity
FROM retail_transactions
WHERE "Quantity" <= 0;

SELECT COUNT(*) AS invalid_price
FROM retail_transactions
WHERE "Price" <= 0;

-- 5. Cek TotalAmount negatif
SELECT COUNT(*) AS negative_total
FROM retail_transactions
WHERE "TotalAmount" < 0;

-- 6. Cek baris dengan TotalAmount tidak sesuai rumus
SELECT COUNT(*) AS mismatch_total
FROM retail_transactions
WHERE ABS(
    ("Quantity" * "Price" * (1 - "DiscountApplied(%)" / 100.0)) - "TotalAmount"
) > 0.01;

-- 7. Distribusi ProductCategory (untuk sanity check)
SELECT "ProductCategory", COUNT(*) AS cnt
FROM retail_transactions
GROUP BY "ProductCategory"
ORDER BY cnt DESC;