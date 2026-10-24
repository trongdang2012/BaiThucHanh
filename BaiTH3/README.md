# HỆ THỐNG QUẢN LÝ SẢN PHẨM (PRODUCT MANAGEMENT SYSTEM - SOA)

## 1. Giới thiệu kiến trúc
Hệ thống được thiết kế theo kiến trúc Hướng dịch vụ (SOA - Service-Oriented Architecture):
- **Auth Service (Port 5000)**: Dịch vụ xác thực độc lập. Cung cấp API và giao diện quản lý đăng nhập, cấp phát và kiểm tra JWT Token.
- **Product Service (Port 5001)**: Dịch vụ quản lý sản phẩm hoạt động độc lập trên cổng 5001 với cơ sở dữ liệu riêng SQLite (`products.db`). Xác thực phân quyền thông qua Auth Service.
- **Web Clients**: Giao diện web trực quan cho cả 2 dịch vụ, liên kết chéo qua lại, hỗ trợ đầy đủ các thao tác tìm kiếm, lọc, thống kê và quản lý sản phẩm.

---

## 2. Cấu trúc thư mục
```
BaiTH3/
│
├── auth_service/                # Dịch vụ xác thực (Port 5000)
│   └── main.py                  # API xác thực & Giao diện Auth Console (http://localhost:5000/)
│
├── product_service/             # Dịch vụ quản lý sản phẩm (Port 5001)
│   ├── database.py              # Kết nối và khởi tạo CSDL SQLite riêng biệt
│   ├── models.py                # Mô hình đối tượng sản phẩm
│   ├── schemas.py               # Pydantic schemas (Request / Response validation)
│   ├── controllers.py           # Controller xử lý nghiệp vụ và truy vấn CSDL
│   ├── auth_client.py           # Giao tiếp xác thực token qua Auth Service
│   └── main.py                  # Khai báo RESTful API endpoints & phục vụ Web UI
│
├── client/                      # Giao diện Web Client quản lý sản phẩm
│   ├── index.html               # Trang giao diện chính
│   ├── style.css                # Bộ định dạng phong cách hiện đại
│   └── app.js                   # Xử lý logic gọi API và hiển thị
│
├── run.bat                      # File khởi động cả 2 service và tự động mở Web Client
├── stop.bat                     # File tắt các service an toàn
├── test_api.py                  # Script kiểm thử tự động toàn diện
└── requirements.txt             # Danh sách thư viện phụ thuộc
```

---

## 3. Cấu trúc bảng CSDL `products`
| Tên cột | Kiểu dữ liệu | Mô tả |
| :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | ID duy nhất của sản phẩm |
| `name` | VARCHAR(255) NOT NULL | Tên sản phẩm |
| `description` | TEXT | Mô tả sản phẩm |
| `price` | DECIMAL(10, 2) NOT NULL | Giá sản phẩm |
| `quantity` | INTEGER NOT NULL DEFAULT 0 | Số lượng sản phẩm trong kho |
| `created_at` | TIMESTAMP | Ngày sản phẩm được tạo |
| `updated_at` | TIMESTAMP | Ngày sản phẩm được cập nhật lần cuối |

---

## 4. Danh sách RESTful API
### Product Service (Port 5001)
| Phương thức | Đường dẫn (Endpoint) | Quyền truy cập | Mô tả |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Công khai | Giao diện Web Quản lý sản phẩm |
| **GET** | `/products` | Công khai | Lấy danh sách tất cả các sản phẩm |
| **GET** | `/products/{id}` | Công khai | Lấy thông tin chi tiết một sản phẩm theo ID |
| **POST** | `/products` | Cần Bearer Token | Thêm mới một sản phẩm |
| **PUT** | `/products/{id}` | Cần Bearer Token | Cập nhật thông tin sản phẩm |
| **DELETE** | `/products/{id}` | Cần Bearer Token | Xóa một sản phẩm theo ID |

### Auth Service (Port 5000)
| Phương thức | Đường dẫn (Endpoint) | Mô tả |
| :--- | :--- | :--- |
| **GET** | `/` | Giao diện Auth Console (Đăng nhập, test token trực tiếp) |
| **POST** | `/login` | Đăng nhập cấp phát JWT Token |
| **GET** | `/auth` | Xác thực Bearer Token hợp lệ |

---

## 5. Hướng dẫn sử dụng
1. Khởi động hệ thống: Nhấp đúp chuột vào file **`run.bat`**.
2. Hệ thống sẽ tự động mở đồng thời cả 2 dịch vụ trên trình duyệt:
   - Giao diện Quản lý sản phẩm: **http://localhost:5001/**
   - Giao diện Xác thực Auth Service: **http://localhost:5000/**
3. Tài khoản mặc định: `admin` / `admin123`.
4. Trên thanh điều hướng của mỗi giao diện đều có nút liên kết nhanh để chuyển đổi qua lại giữa 2 dịch vụ hoặc mở tài liệu Swagger API Docs.
