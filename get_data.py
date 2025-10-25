import pandas as pd
import json
import os
from vnstock import financial_report

# ---- BƯỚC 1: Đọc file cấu hình (config.json) ----
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

symbol = config.get("symbol", "FPT")  # Mã doanh nghiệp
report_type = config.get("report_type", "incomestatement")  # income/cashflow/balance
year = config.get("year", 2025)
quarter = config.get("quarter", 2)

# ---- BƯỚC 2: Gọi API từ vnstock ----
try:
    df = financial_report(symbol=symbol, report_type=report_type, frequency='quarterly')
except Exception as e:
    print(f"❌ Lỗi khi gọi dữ liệu từ vnstock: {e}")
    exit()

# ---- BƯỚC 3: Lọc theo quý và năm yêu cầu ----
df_filtered = df[(df['year'] == year) & (df['quarter'] == quarter)]

# ---- BƯỚC 4: Tạo thư mục nếu chưa có ----
os.makedirs("data", exist_ok=True)

# ---- BƯỚC 5: Lưu file ----
filename = f"data/{symbol.lower()}_q{quarter}_{year}.csv"
df_filtered.to_csv(filename, index=False, encoding="utf-8-sig")

print(f"✅ Đã lưu dữ liệu: {filename}")
