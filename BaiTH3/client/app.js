const AUTH_API = "http://localhost:5000";
const PRODUCT_API = "http://localhost:5001";

let state = {
    token: localStorage.getItem("soa_jwt_token") || "",
    username: localStorage.getItem("soa_username") || "",
    products: []
};

document.addEventListener("DOMContentLoaded", () => {
    initUI();
    checkServices();
    fetchProducts();
    setupEvents();
});

function initUI() {
    updateAuthUI();
}

function updateAuthUI() {
    const userInfoEl = document.getElementById("user-info");
    const btnOpenLogin = document.getElementById("btn-open-login");
    const userNameEl = document.getElementById("user-name");
    const statJwt = document.getElementById("stat-jwt-status");

    if (state.token) {
        userInfoEl.classList.remove("hidden");
        btnOpenLogin.classList.add("hidden");
        userNameEl.textContent = state.username || "admin";
        statJwt.textContent = "Đã xác thực";
        statJwt.classList.remove("text-muted");
        statJwt.style.color = "#059669";
    } else {
        userInfoEl.classList.add("hidden");
        btnOpenLogin.classList.remove("hidden");
        statJwt.textContent = "Chưa có token";
        statJwt.classList.add("text-muted");
        statJwt.style.color = "";
    }
}

async function checkServices() {
    const authBadge = document.getElementById("badge-auth");
    const prodBadge = document.getElementById("badge-product");

    try {
        const res = await fetch(`${AUTH_API}/health`, { method: "GET" });
        if (res.ok) {
            authBadge.className = "status-badge online";
            authBadge.innerHTML = '<span class="dot"></span> Auth Service (5000)';
        } else {
            throw new Error();
        }
    } catch {
        authBadge.className = "status-badge offline";
        authBadge.innerHTML = '<span class="dot"></span> Auth Service (Offline)';
    }

    try {
        const res = await fetch(`${PRODUCT_API}/health`, { method: "GET" });
        if (res.ok) {
            prodBadge.className = "status-badge online";
            prodBadge.innerHTML = '<span class="dot"></span> Product Service (5001)';
        } else {
            throw new Error();
        }
    } catch {
        prodBadge.className = "status-badge offline";
        prodBadge.innerHTML = '<span class="dot"></span> Product Service (Offline)';
    }
}

async function fetchProducts() {
    const tbody = document.getElementById("product-table-body");
    const emptyState = document.getElementById("empty-state");

    try {
        const res = await fetch(`${PRODUCT_API}/products`);
        if (!res.ok) throw new Error("Không thể tải danh sách sản phẩm");
        const data = await res.json();
        state.products = data;
        renderProducts(data);
        updateStats(data);
    } catch (err) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="loading-cell" style="color: var(--danger)">
                    Không thể kết nối đến Product Service (Port 5001). Vui lòng đảm bảo service đang chạy!
                </td>
            </tr>
        `;
        emptyState.classList.add("hidden");
    }
}

function updateStats(items) {
    const totalCount = items.length;
    const totalQty = items.reduce((sum, item) => sum + (Number(item.quantity) || 0), 0);
    const totalValue = items.reduce((sum, item) => sum + ((Number(item.price) || 0) * (Number(item.quantity) || 0)), 0);

    document.getElementById("stat-total-count").textContent = totalCount;
    document.getElementById("stat-total-qty").textContent = totalQty.toLocaleString("vi-VN");
    document.getElementById("stat-total-value").textContent = totalValue.toLocaleString("vi-VN") + " đ";
}

function renderProducts(items) {
    const tbody = document.getElementById("product-table-body");
    const emptyState = document.getElementById("empty-state");

    if (!items || items.length === 0) {
        tbody.innerHTML = "";
        emptyState.classList.remove("hidden");
        return;
    }

    emptyState.classList.add("hidden");
    tbody.innerHTML = items.map(p => {
        const qty = Number(p.quantity) || 0;
        let qtyBadgeClass = "qty-in-stock";
        let qtyLabel = `${qty} cái`;
        if (qty === 0) {
            qtyBadgeClass = "qty-out";
            qtyLabel = "Hết hàng";
        } else if (qty < 5) {
            qtyBadgeClass = "qty-low";
            qtyLabel = `${qty} (Sắp hết)`;
        }

        const priceFmt = (Number(p.price) || 0).toLocaleString("vi-VN") + " đ";

        return `
            <tr>
                <td><strong>#${p.id}</strong></td>
                <td><strong style="color: var(--slate-900)">${escapeHtml(p.name)}</strong></td>
                <td><span style="color: var(--slate-500); font-size: 13px;">${escapeHtml(p.description || "—")}</span></td>
                <td><span class="price-text">${priceFmt}</span></td>
                <td><span class="qty-badge ${qtyBadgeClass}">${qtyLabel}</span></td>
                <td style="font-size: 13px; color: var(--slate-500)">${escapeHtml(p.updated_at || p.created_at || "—")}</td>
                <td>
                    <div class="table-actions">
                        <button class="btn-action" title="Xem chi tiết" onclick="viewDetail(${p.id})">Xem</button>
                        <button class="btn-action" title="Chỉnh sửa" onclick="openEditModal(${p.id})">Sửa</button>
                        <button class="btn-action delete" title="Xóa" onclick="deleteProduct(${p.id})">Xóa</button>
                    </div>
                </td>
            </tr>
        `;
    }).join("");
}

function setupEvents() {
    document.getElementById("btn-refresh").addEventListener("click", () => {
        checkServices();
        fetchProducts();
        showToast("Đã làm mới dữ liệu", "info");
    });

    document.getElementById("input-search").addEventListener("input", (e) => {
        const q = e.target.value.toLowerCase().trim();
        const filtered = state.products.filter(p => 
            p.name.toLowerCase().includes(q) || 
            (p.description && p.description.toLowerCase().includes(q))
        );
        renderProducts(filtered);
    });

    document.getElementById("btn-open-add").addEventListener("click", () => {
        if (!state.token) {
            showToast("Vui lòng đăng nhập qua Auth Service để thêm sản phẩm!", "error");
            openModal("modal-login");
            return;
        }
        document.getElementById("modal-product-title").textContent = "Thêm sản phẩm mới";
        document.getElementById("form-product").reset();
        document.getElementById("product-id").value = "";
        openModal("modal-product");
    });

    document.getElementById("btn-open-login").addEventListener("click", () => {
        openModal("modal-login");
    });

    document.getElementById("btn-logout").addEventListener("click", () => {
        state.token = "";
        state.username = "";
        localStorage.removeItem("soa_jwt_token");
        localStorage.removeItem("soa_username");
        updateAuthUI();
        showToast("Đã đăng xuất tài khoản", "info");
    });

    document.getElementById("form-product").addEventListener("submit", handleSaveProduct);
    document.getElementById("form-login").addEventListener("submit", handleLogin);

    document.querySelectorAll("[data-close]").forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-close");
            closeModal(targetId);
        });
    });

    window.addEventListener("click", (e) => {
        if (e.target.classList.contains("modal-backdrop")) {
            e.target.classList.add("hidden");
        }
    });
}

async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value.trim();

    try {
        const res = await fetch(`${AUTH_API}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ userName: username, password: password })
        });

        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.detail || "Đăng nhập thất bại");
        }

        state.token = data.token;
        state.username = username;
        localStorage.setItem("soa_jwt_token", data.token);
        localStorage.setItem("soa_username", username);

        updateAuthUI();
        closeModal("modal-login");
        showToast("Đăng nhập và lấy JWT Token thành công!", "success");
    } catch (err) {
        showToast(err.message, "error");
    }
}

async function handleSaveProduct(e) {
    e.preventDefault();
    if (!state.token) {
        showToast("Phiên làm việc hết hạn. Vui lòng đăng nhập lại!", "error");
        openModal("modal-login");
        return;
    }

    const id = document.getElementById("product-id").value;
    const name = document.getElementById("product-name").value.trim();
    const description = document.getElementById("product-description").value.trim();
    const price = parseFloat(document.getElementById("product-price").value);
    const quantity = parseInt(document.getElementById("product-quantity").value, 10);

    const payload = { name, description, price, quantity };

    const isEdit = Boolean(id);
    const url = isEdit ? `${PRODUCT_API}/products/${id}` : `${PRODUCT_API}/products`;
    const method = isEdit ? "PUT" : "POST";

    try {
        const res = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${state.token}`
            },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.detail || "Không thể lưu sản phẩm");
        }

        closeModal("modal-product");
        showToast(isEdit ? "Cập nhật sản phẩm thành công!" : "Thêm mới sản phẩm thành công!", "success");
        fetchProducts();
    } catch (err) {
        showToast(err.message, "error");
    }
}

window.openEditModal = function(id) {
    if (!state.token) {
        showToast("Vui lòng đăng nhập qua Auth Service để chỉnh sửa!", "error");
        openModal("modal-login");
        return;
    }

    const item = state.products.find(p => p.id === id);
    if (!item) return;

    document.getElementById("modal-product-title").textContent = `Chỉnh sửa sản phẩm #${id}`;
    document.getElementById("product-id").value = item.id;
    document.getElementById("product-name").value = item.name;
    document.getElementById("product-description").value = item.description || "";
    document.getElementById("product-price").value = item.price;
    document.getElementById("product-quantity").value = item.quantity;

    openModal("modal-product");
};

window.deleteProduct = async function(id) {
    if (!state.token) {
        showToast("Vui lòng đăng nhập qua Auth Service để xóa sản phẩm!", "error");
        openModal("modal-login");
        return;
    }

    if (!confirm(`Bạn có chắc chắn muốn xóa sản phẩm ID #${id} không?`)) {
        return;
    }

    try {
        const res = await fetch(`${PRODUCT_API}/products/${id}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${state.token}`
            }
        });

        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.detail || "Không thể xóa sản phẩm");
        }

        showToast(`Đã xóa thành công sản phẩm #${id}`, "success");
        fetchProducts();
    } catch (err) {
        showToast(err.message, "error");
    }
};

window.viewDetail = function(id) {
    const item = state.products.find(p => p.id === id);
    if (!item) return;

    document.getElementById("detail-id").textContent = `#${item.id}`;
    document.getElementById("detail-name").textContent = item.name;
    document.getElementById("detail-description").textContent = item.description || "Không có mô tả.";
    document.getElementById("detail-price").textContent = (Number(item.price) || 0).toLocaleString("vi-VN") + " đ";
    document.getElementById("detail-quantity").textContent = `${item.quantity} cái`;
    document.getElementById("detail-created-at").textContent = item.created_at || "—";
    document.getElementById("detail-updated-at").textContent = item.updated_at || "—";

    openModal("modal-detail");
};

function openModal(id) {
    document.getElementById(id).classList.remove("hidden");
}

function closeModal(id) {
    document.getElementById(id).classList.add("hidden");
}

function showToast(msg, type = "info") {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = msg;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(50px)";
        toast.style.transition = "all 0.3s";
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}

function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
