from typing import List, Optional
from datetime import datetime
from sqlite3 import Connection
from schemas import ProductCreate, ProductUpdate

def row_to_dict(row) -> Optional[dict]:
    if row is None:
        return None
    return dict(row)

def get_all_products(conn: Connection) -> List[dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY id ASC")
    rows = cursor.fetchall()
    return [row_to_dict(row) for row in rows]

def get_product_by_id(conn: Connection, product_id: int) -> Optional[dict]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    return row_to_dict(row)

def create_product(conn: Connection, product_in: ProductCreate) -> dict:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO products (name, description, price, quantity, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (product_in.name, product_in.description, product_in.price, product_in.quantity, now, now)
    )
    conn.commit()
    new_id = cursor.lastrowid
    return get_product_by_id(conn, new_id)

def update_product(conn: Connection, product_id: int, product_in: ProductUpdate) -> Optional[dict]:
    existing = get_product_by_id(conn, product_id)
    if not existing:
        return None

    update_fields = []
    values = []

    if product_in.name is not None:
        update_fields.append("name = ?")
        values.append(product_in.name)

    if product_in.description is not None:
        update_fields.append("description = ?")
        values.append(product_in.description)

    if product_in.price is not None:
        update_fields.append("price = ?")
        values.append(product_in.price)

    if product_in.quantity is not None:
        update_fields.append("quantity = ?")
        values.append(product_in.quantity)

    if not update_fields:
        return existing

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_fields.append("updated_at = ?")
    values.append(now)

    values.append(product_id)
    sql = f"UPDATE products SET {', '.join(update_fields)} WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, tuple(values))
    conn.commit()

    return get_product_by_id(conn, product_id)

def delete_product(conn: Connection, product_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    return cursor.rowcount > 0
