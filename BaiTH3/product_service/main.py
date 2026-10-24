import os
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

from database import init_db, get_db
from schemas import ProductCreate, ProductUpdate, ProductResponse
from controllers import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)
from auth_client import verify_token

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Product Management Service",
    description="Dich vu quan ly san pham theo kien truc SOA - Port 5001",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLIENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "client"))
if os.path.exists(CLIENT_DIR):
    @app.get("/", include_in_schema=False)
    def serve_client_app():
        return FileResponse(os.path.join(CLIENT_DIR, "index.html"))

    @app.get("/style.css", include_in_schema=False)
    def serve_css():
        return FileResponse(os.path.join(CLIENT_DIR, "style.css"))

    @app.get("/app.js", include_in_schema=False)
    def serve_js():
        return FileResponse(os.path.join(CLIENT_DIR, "app.js"))

@app.get("/products", response_model=List[ProductResponse])
def read_all_products():
    with get_db() as conn:
        return get_all_products(conn)

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int):
    with get_db() as conn:
        item = get_product_by_id(conn, product_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"San pham co ID {product_id} khong ton tai"
            )
        return item

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(
    product_in: ProductCreate,
    current_user: dict = Depends(verify_token)
):
    with get_db() as conn:
        return create_product(conn, product_in)

@app.put("/products/{product_id}", response_model=ProductResponse)
def edit_product(
    product_id: int,
    product_in: ProductUpdate,
    current_user: dict = Depends(verify_token)
):
    with get_db() as conn:
        updated = update_product(conn, product_id, product_in)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"San pham co ID {product_id} khong ton tai de cap nhat"
            )
        return updated

@app.delete("/products/{product_id}")
def remove_product(
    product_id: int,
    current_user: dict = Depends(verify_token)
):
    with get_db() as conn:
        success = delete_product(conn, product_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"San pham co ID {product_id} khong ton tai de xoa"
            )
        return {"message": f"Da xoa thanh cong san pham ID {product_id}"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "product_service", "port": 5001}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
