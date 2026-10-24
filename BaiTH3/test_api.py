import requests
import json

AUTH_URL = "http://localhost:5000"
PRODUCT_URL = "http://localhost:5001"

def print_result(title, status_code, body):
    print(f"\n--- {title} ---")
    print(f"Status Code: {status_code}")
    try:
        print(json.dumps(body, indent=2, ensure_ascii=False))
    except Exception:
        print(body)

def main():
    print("BAT DAU KIEM THU HE THONG (SOA - PRODUCT & AUTH SERVICES)...")
    
    # 1. Dang nhap lay JWT token tu Auth Service
    login_data = {
        "userName": "admin",
        "password": "admin123"
    }
    res = requests.post(f"{AUTH_URL}/login", json=login_data)
    print_result("1. Dang nhap Auth Service", res.status_code, res.json())
    assert res.status_code == 200, "Dang nhap that bai"
    token = res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Kiem tra xac thuc token tai Auth Service
    res = requests.get(f"{AUTH_URL}/auth", headers=headers)
    print_result("2. Xac thuc token tai Auth Service", res.status_code, res.json())
    assert res.status_code == 200, "Token khong hop le"

    # 3. Kiem tra them san pham KHONG kem token
    sample_product = {
        "name": "Laptop Dell XPS 15",
        "description": "Laptop cao cap danh cho lap trinh vien",
        "price": 28500000.0,
        "quantity": 10
    }
    res = requests.post(f"{PRODUCT_URL}/products", json=sample_product)
    print_result("3. Them san pham KHONG kem token (Test bao mat)", res.status_code, res.json())
    assert res.status_code == 401, "He thong chua chan truy cap trai phep"

    # 4. Them san pham CO token xac thuc
    res = requests.post(f"{PRODUCT_URL}/products", json=sample_product, headers=headers)
    print_result("4. Them san pham CO token", res.status_code, res.json())
    assert res.status_code == 201, "Them san pham that bai"
    created_product = res.json()
    product_id = created_product["id"]

    # 5. Lay danh sach tat ca san pham
    res = requests.get(f"{PRODUCT_URL}/products")
    print_result("5. Lay danh sach tat ca san pham", res.status_code, res.json())
    assert res.status_code == 200, "Lay danh sach that bai"

    # 6. Lay chi tiet san pham theo ID
    res = requests.get(f"{PRODUCT_URL}/products/{product_id}")
    print_result(f"6. Lay chi tiet san pham ID {product_id}", res.status_code, res.json())
    assert res.status_code == 200, "Lay chi tiet that bai"

    # 7. Cap nhat san pham theo ID (PUT)
    update_data = {
        "price": 27000000.0,
        "quantity": 15
    }
    res = requests.put(f"{PRODUCT_URL}/products/{product_id}", json=update_data, headers=headers)
    print_result(f"7. Cap nhat san pham ID {product_id}", res.status_code, res.json())
    assert res.status_code == 200, "Cap nhat that bai"

    # 8. Xoa san pham theo ID (DELETE)
    res = requests.delete(f"{PRODUCT_URL}/products/{product_id}", headers=headers)
    print_result(f"8. Xoa san pham ID {product_id}", res.status_code, res.json())
    assert res.status_code == 200, "Xoa that bai"

    # 9. Kiem tra lai san pham da xoa
    res = requests.get(f"{PRODUCT_URL}/products/{product_id}")
    print_result(f"9. Kiem tra san pham sau khi xoa ID {product_id}", res.status_code, res.json())
    assert res.status_code == 404, "San pham chua duoc xoa"

    print("\nTAT CA CAC TEST CASE DA HOAN THANH VA XAC THUC THANH CONG!")

if __name__ == "__main__":
    main()
