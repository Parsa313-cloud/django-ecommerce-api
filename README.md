<div align="center">

# 🛒 Django E-Commerce API

**A robust, scalable, and fully documented RESTful API for an E-commerce platform.**


![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<br>

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)]()
[![Django REST Framework](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)]()
[![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)]()
[![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)]()

</div>

---


## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Entity-Relationship Diagram (ERD)](#-entity-relationship-diagram-erd)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Environment Variables](#-environment-variables)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [License](#-license)

---

## 🚀 About the Project

This project is a comprehensive REST API backend for an E-commerce application. It handles everything from user authentication and profile management to product cataloging, shopping cart operations, and order processing. The API is designed with best practices in mind, utilizing JSON Web Tokens (JWT) for secure authentication and Swagger UI for interactive, real-time documentation.

---

## ✨ Key Features

- **🔐 Secure Authentication:** JWT-based login and registration system.
- **👤 User Management:** Custom user models with extended profiles (address, phone number, automated slugs).
- **🛍️ Product Catalog:** Categorized products with UUID-based public IDs and real-time inventory tracking (preventing negative balances).
- **🛒 Shopping Cart System:** One-to-one cart per user, dynamic cart items, and order generation.
- **📚 Interactive Docs:** Auto-generated Swagger UI and Redoc via `drf-spectacular`.
- **🛡️ Data Security:** Environment variables management using `python-dotenv` to protect sensitive credentials.

---

## 📊 Entity-Relationship Diagram (ERD)

Here is the database schema detailing the relationships between Users, Profiles, Products, Carts, and Orders:

<div align="center">
  <img src="./images/erd.png" alt="E-commerce Database ERD" width="800">
</div>


---

## 🛠️ Tech Stack

- **Framework:** Django 5.2.7, Django REST Framework 3.16.1
- **Database:** PostgreSQL
- **Authentication:** SimpleJWT (`djangorestframework-simplejwt`)
- **Documentation:** Swagger UI / Redoc (`drf-spectacular`)
- **Utilities:** `django-filter`, `django-phonenumber-field`, `python-dotenv`

---

## 🏁 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing.

### Prerequisites

Make sure you have the following installed:
- Python 3.10+
- PostgreSQL
- Git

### Installation

1. **Clone the repository:**
   git clone https://github.com/YourUsername/your-repo-name.git
   cd your-repo-name

2. **Create and activate a virtual environment:**
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

3. **Install dependencies:**
   pip install -r requirements.txt

4. **Set up environment variables:**
   Copy the example environment file and fill in your details:
   cp .env.example .env
   *(See the Environment Variables section for details)*

5. **Apply database migrations:**
   python manage.py migrate

6. **Create a superuser (optional but recommended):**
   python manage.py createsuperuser

7. **Run the development server:**
   python manage.py runserver

---

## 🔐 Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file. You can use the provided `.env.example` as a template.

# Django Settings
SECRET_KEY=your_super_secret_django_key_here
DEBUG=True

# Database Settings (PostgreSQL)
DB_NAME=your_db_name
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=5432

---

## 📚 API Documentation

This API is fully documented using Swagger. Once your local server is running, you can access the interactive documentation to explore and test the endpoints directly from your browser:

- **Swagger UI:** http://127.0.0.1:8000/api/docs/
- **OpenAPI Schema:** http://127.0.0.1:8000/api/schema/

---

## 📁 Project Structure

📦 e_commerce_project
 ┣ 📂 accounts         # User authentication and profile models/views
 ┣ 📂 products         # Product catalog and categories
 ┣ 📂 cart             # Shopping cart and order items logic
 ┣ 📂 core             # Main Django settings and URLs
 ┣ 📜 .env             # Environment variables (Ignored in Git)
 ┣ 📜 .env.example     # Template for environment variables
 ┣ 📜 requirements.txt # Project dependencies
 ┗ 📜 manage.py

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
<div align="center">
  <i>Developed with ❤️ by [Your Name]</i>
</div>
