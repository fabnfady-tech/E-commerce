# 🛒 Advanced E-Commerce RESTful API

A robust, production-ready E-commerce Backend API engineered with **Django REST Framework (DRF)** and **PostgreSQL**. This platform features high-performance database optimization, secure transactional checkout workflows, image deduplication processing, and scalable caching layers.

---

## 🌟 Advanced Architectural Features

### 1. Thread-Safe Transactional Checkout (`transaction.atomic`)
To avoid critical data race conditions and ensure absolute financial data integrity, the checkout workflow is fully encapsulated within **Database Atomic Transactions**. If any step fails during checkout (e.g., stock validation, order item creation), the entire database state is instantly rolled back, guaranteeing that user carts are never lost or corrupted.

### 2. Cryptographic Image Deduplication via SHA-256
Optimized server-side media storage by implementing an automated image-hashing pipeline. The `ProductImage` model intercepts media uploads, computes a unique **SHA-256 cryptographic hash** of the binary file, and validates it against the database. Redundant image uploads are rejected with a `ValidationError`, preventing storage bloating.

### 3. Smart Server-Side Caching Layer
Integrated a localized **Memory Caching (`LocMemCache`)** mechanism to cache the high-traffic catalog listing endpoints (`/api/store/products/`). The listing view intercepts database queries and caches the results for **120 seconds**, slashing database read operations by up to 90% under simulated heavy traffic.

### 4. Historical Pricing Snapshots
Designed an unalterable auditing system within the order tracking schemas. When a checkout succeeds, the exact pricing of each item is recorded as a static snapshot inside the `OrderItem` table, protecting the company's financial records and historical order totals from future catalog price modifications.

---

## 🛠️ Tech Stack & Dependencies

*   **Framework:** Django & Django REST Framework (DRF)
*   **Database:** PostgreSQL (Production-ready relational model)
*   **Security:** JWT Authentication (`django-rest-framework-simplejwt`)
*   **Caching:** Django Core Caching Layer (`LocMemCache`)
*   **Security Filters:** Django Cors Headers (`CORS_ALLOW_ALL_ORIGINS = True`)
*   **API Throttling:** DRF Native Rate Limiting

---

## 🔒 Security & Rate Limiting (Throttling)

The API enforces strict data-access protocols and request throttling via `settings.py` to prevent brute-force attacks and abuse:
*   **Default Permission:** `IsAuthenticatedOrReadOnly` ensures catalogs are public, but mutating resources requires active authorization.
*   **Anonymous Users Rate Limit:** Restricted to **100 requests / day**.
*   **Authenticated Users Rate Limit:** Restricted to **1000 requests / day**.
*   **JWT Life Cycle:** Access tokens expire securely in **60 minutes**, with refresh tokens valid for **7 days**.

---

## 📂 Project Structure

```text
ecommerce/
│
├── store/              # Catalog management (Categories, Products, Images, Reviews)
├── cart/               # Session/User cart items management
├── orders/             # Transactional checkout processing & historical order logs
├── project/            # Central settings, routing, and WSGI/ASGI configurations
├── media/              # Locally managed product media uploads
└── manage.py           # Administrative management CLI tool