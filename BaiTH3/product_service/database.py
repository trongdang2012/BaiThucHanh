import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "products.db")

SAMPLE_PRODUCTS = [
    {
        "name": "Laptop Dell XPS 13 Plus",
        "description": "Intel Core i7 1360P, 16GB RAM, 512GB SSD, màn hình 3.5K OLED cảm ứng.",
        "price": 32500000.0,
        "quantity": 8
    },
    {
        "name": "MacBook Pro 14 M3",
        "description": "Chip Apple M3 Pro, 18GB Unified Memory, 512GB SSD, vỏ nhôm Space Black.",
        "price": 48990000.0,
        "quantity": 5
    },
    {
        "name": "Bàn phím cơ Keychron K2 Pro",
        "description": "Kết nối không dây Bluetooth 5.1, switch Gateron Pro Red, layout 75% gọn gàng.",
        "price": 2150000.0,
        "quantity": 24
    },
    {
        "name": "Chuột không dây Logitech MX Master 3S",
        "description": "Cảm biến Darkfield 8000 DPI, cuộn MagSpeed siêu tốc, nút bấm Silent Switch.",
        "price": 2490000.0,
        "quantity": 15
    },
    {
        "name": "Màn hình Dell UltraSharp U2724D",
        "description": "27 inch 2K QHD IPS Black, tần số quét 120Hz, màu sắc 98% DCI-P3 chuẩn đồ họa.",
        "price": 9800000.0,
        "quantity": 12
    },
    {
        "name": "Tai nghe chống ồn Sony WH-1000XM5",
        "description": "Chống ồn chủ động cao cấp, thời lượng pin 30 giờ liên tục, hỗ trợ Hi-Res Audio.",
        "price": 6790000.0,
        "quantity": 18
    },
    {
        "name": "Ổ cứng SSD Samsung 990 Pro 1TB",
        "description": "Chuẩn PCIe 4.0 NVMe, tốc độ đọc 7450 MB/s, ghi 6900 MB/s cho máy trạm.",
        "price": 2850000.0,
        "quantity": 30
    },
    {
        "name": "Ghế công thái học Herman Miller Aeron",
        "description": "Chất liệu lưới Pellicle thoáng khí, đệm tựa PostureFit SL chuẩn công thái học.",
        "price": 29500000.0,
        "quantity": 3
    }
]

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for item in SAMPLE_PRODUCTS:
            cursor.execute(
                """
                INSERT INTO products (name, description, price, quantity, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (item["name"], item["description"], item["price"], item["quantity"], now, now)
            )
        conn.commit()

    conn.close()

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
