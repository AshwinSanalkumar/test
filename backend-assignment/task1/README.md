# Assignment API TASK-1

A REST API built with **Django** and **Django REST Framework** that supports secure file uploads and downloads via one-time secure links, product management operations, and authentication using JSON Web Tokens (JWT).

---

## Features

* **Product Management (CRUD)**: Full lifecycle management for products including image uploads.
* **Soft Delete Logic**: Products are marked as is_deleted rather than removed from the DB, preserving data integrity.    
* **Secure File Upload**: Multi-part file handling with automated MIME-type validation (PDF, PNG, JPG, etc.) and size constraints.
* **One-Time Use Download Links:**: logic that disables a download token(link) immediately after the first successful access, preventing link reuse.
* **Time-Limited Access**: Integrated security window that automatically expires download links after 5 minutes (configurable) to minimize URL exposure.
* **Authentication & Privacy**: Full JWT-based security ensuring users can only manage and share files they own.
---

## Tech Stack

* **Python**
* **Django**
* **Django REST Framework**
* **python-dotenv**

---

## Project Structure

```text
backend-assignment/
│
├── task1/
|   |
|   ├── api/
|   │   ├── views.py
|   │   ├── urls.py
|   │   ├── models.py
|   │   ├── services.py
|   │   ├── tests.py
|   │   └── serializers.py
|   ├── config/
|   │   ├── settings.py
|   │   └── urls.py
|   ├── .env.example
|   ├── manage.py
|   └── requirements.txt
|
└── task2

```

---

# Installation & Setup

### 1 Clone the repository

```bash
git clone <repository-url>
cd <backend-assignment/task1>
```

### 2 Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3 Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

This project uses environment variables for sensitive settings.

1. Copy the example environment file:

```bash
cp .env-example .env
```

# Run the Project

Apply migrations:

```bash
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

Server runs at:

```
http://127.0.0.1:8000
```

---
# API Endpoints

<details>
<summary><strong>Authentication</strong></summary>

POST /api/register/          #Create new account
POST /api/login/             #login to existing account
POST /api/refresh/           #Generate new Access token using Refresh Token
POST /api/logout/            #logut (blacklist Refresh token)

---
</details>

<details>
<summary><strong>Product Management</strong></summary>

GET /api/products/                             # list Products
POST /api/products/add/                        # Add new products
GET /api/products/view/<product_id>/           # view details of a product
PUT /api/products/update/<product_id>/         # Update a product
DELETE /api/products/delete/<product_id>/      # Delete a Product

---
</details>

<details>
<summary><strong>Secure File Management</strong></summary>

POST /api/files/upload/                        # Upload a file
GET /api/files/list/                           # List the uploaded files
POST /api/files/<file_id>/generate-link/       # Genrate secure Download link 
GET /api/file/download/<token>/                # Download the file

</details>

# Security Notes

* `.env` file is excluded from version control.
* `.env.example` provides the required environment variables.

---

# Author

Ashwin Sanalkumar

---