# StockWise: Multi-Tenant Inventory & Warehouse Management System

StockWise is a full-featured inventory and warehouse management system built with **Django REST Framework (DRF)** on the backend and modern vanilla **HTML5 / Bootstrap 5 / JavaScript** on the frontend. It supports multi-tenancy by company, strict role-based access control (RBAC), real-time stock transactions, and inventory reorder alerts.

---

## 🚀 Key Features

- **Company Multi-Tenancy**: Data isolation across different companies. Users only access catalog, warehouses, inventory, and stock logs belonging to their company.
- **Role-Based Access Control (RBAC)**:
  - **System Admin**: Global oversight across companies and users.
  - **Admin**: Full administrative control over company users, categories, products, warehouses, and role promotions.
  - **Manager**: Warehouse and inventory management, role updating for subordinate roles, stock auditing.
  - **Store Keeper**: Stock transactions (Receive, Issue, Return, Adjustment) and inventory operations.
  - **Staff / Auditor**: Read-only access to catalogs, stock levels, and transaction reports.
- **Automated SKU & Warehouse Code Generation**: Dynamic alphanumeric code assignment on creation.
- **Atomic Stock Transactions**:
  - Thread-safe, concurrent transaction handling (`select_for_update` + `@transaction.atomic`).
  - Supports `Receive`, `Issue`, `Return`, and `Adjustment` transaction types.
  - Prevents negative stock issues and maintains an immutable audit log.
- **Inventory Tracking & Low Stock Alerts**: Automatic status calculation (`Normal`, `Reorder`, `Critical`) and dedicated low-stock views.
- **JWT Authentication & Token Blacklisting**: Secure login, access token refresh, and complete server-side logout.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.12+, Django 5.2, Django REST Framework, SimpleJWT, django-filter, django-cors-headers, psycopg 3
- **Database**: PostgreSQL
- **Frontend**: HTML5, Vanilla JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons
- **Security**: Decouple environment secrets, password validators, CORS controls, role permissions

---

## 📂 Project Structure

```
inventory_and_warehouse_management/
├── backend/
│   ├── manage.py
│   ├── config/              # Django core settings, URLs, ASGI/WSGI
│   ├── companies/           # Company creation, multi-tenant grouping
│   ├── users/               # Custom User model, auth endpoints, roles
│   ├── warehouses/          # Warehouse locations, capacities, managers
│   └── inventory/           # Categories, Products, Inventory, Stock Transactions
├── frontend/
│   ├── index.html           # Landing page
│   ├── login.html           # Authentication portal
│   ├── register_page.html   # User registration
│   ├── company.html         # Company creation
│   ├── dashboard.html       # Analytics & summary overview
│   ├── product.html         # Product catalog management
│   ├── category.html        # Category management
│   ├── warehouse.html       # Warehouse management
│   ├── inventory.html       # Total inventory tracking
│   ├── low_stock.html       # Critical reorder alerts
│   ├── stock_transaction.html # Stock transaction logs
│   ├── update_role.html     # Employee role assignment
│   ├── js/                  # API clients and page logic
│   └── style/               # Custom responsive styles
├── requirements.txt         # Python package dependencies
├── .env.example             # Template for environment configuration
└── README.md                # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.10+ installed
- PostgreSQL installed and running
- A modern web browser

### 2. Clone the Repository
```bash
git clone <repository-url>
cd inventory_and_warehouse_management
```

### 3. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` into `backend/.env`:
```bash
cp .env.example backend/.env
```
Edit `backend/.env` with your PostgreSQL database credentials and generate a secure `SECRET_KEY`:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Run Database Migrations
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
```bash
python manage.py runserver
```
The Django REST backend API will be available at `http://127.0.0.1:8000/`.

---

## 💻 Running the Frontend

You can serve the frontend with any static HTTP server or VS Code Live Server:

### Option A: VS Code Live Server
1. Open the project in VS Code.
2. Right-click `frontend/index.html` and select **"Open with Live Server"** (default port `5500`).

### Option B: Python HTTP Server
```bash
cd frontend
python -m http.server 5500
```
Open `http://127.0.0.1:5500` in your web browser.

---

## 🔑 User Onboarding Flow

1. **Create a Company**: Visit `company.html` to register a new company profile.
2. **First User (Admin)**: The first user to register under that company automatically receives the **Admin** role.
3. **Subsequent Users (Staff)**: Subsequent users who register under that company start with the **Staff** role.
4. **Role Promotions**: The company Admin or Manager can visit `update_role.html` to promote employees to **Manager**, **Store Keeper**, or **Auditor**.

---

## 📡 API Reference Overview

| Endpoint | Methods | Description | Permissions |
|---|---|---|---|
| `/api/login/` | `POST` | Obtain JWT token pair | Public |
| `/api/token/refresh/` | `POST` | Refresh access token | Public |
| `/api/logout/` | `POST` | Blacklist refresh token & logout | Authenticated |
| `/api/profile/` | `GET` | Get logged-in user profile | Authenticated |
| `/api/change_password/` | `PUT` | Change user password | Authenticated |
| `/api/companies/` | `GET, POST, PUT, DELETE` | Company management | Public (create), Admin/SysAdmin |
| `/api/users/` | `GET, POST, PATCH` | User management & role updates | Admin / Manager |
| `/api/categories/` | `GET, POST, PATCH, DELETE` | Product category endpoints | Admin / Manager / Store Keeper |
| `/api/products/` | `GET, POST, PATCH, DELETE` | Product catalog endpoints | Admin / Manager / Store Keeper |
| `/api/warehouses/` | `GET, POST, PATCH, DELETE` | Warehouse records | Admin / Manager / Store Keeper |
| `/api/inventories/` | `GET, PATCH` | Inventory stock counts | Authenticated |
| `/api/inventories/low_stock/` | `GET` | Filtered items needing reorder | Authenticated |
| `/api/stock_transactions/` | `GET, POST` | Immutable audit log of stock movements | Authenticated / Store Keeper |
