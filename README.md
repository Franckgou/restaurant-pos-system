🍽️ Restaurant POS Backend System
Project Overview
This project is the robust backend API for a modern Restaurant Point-of-Sale (POS) system, designed to streamline restaurant operations from employee management and order processing to inventory tracking and sales analysis. Built with FastAPI, SQLAlchemy, and PostgreSQL, it provides a secure, scalable, and efficient foundation for a multi-user application.

It aims to replace a legacy JavaFX system, focusing on creating a powerful and flexible API layer that can serve various frontend clients (web, mobile, or desktop).

Technologies Used
Python 3.9+: Primary programming language.

FastAPI: High-performance web framework for building APIs.

SQLAlchemy: Powerful SQL toolkit and Object-Relational Mapper (ORM) for database interactions.

PostgreSQL: Robust relational database for data storage.

Pydantic: Data validation and settings management (integrated with FastAPI).

JWT (JSON Web Tokens): For secure authentication and authorization.

Bcrypt: For secure password hashing.

Alembic: Database migration tool for schema management.

Project Structure
restaurant-pos-system/
├── app/
│ ├── api/
│ │ ├── **init**.py
│ │ ├── deps.py # FastAPI dependencies (e.g., get_current_user)
│ │ ├── endpoints/
│ │ │ ├── **init**.py
│ │ │ ├── auth.py # API routes for login, password change
│ │ │ ├── employees.py # API routes for Employee CRUD (Implemented)
│ │ │ ├── menu.py # API routes for Menu Item management (Planned)
│ │ │ ├── orders.py # API routes for Order management (Planned)
│ │ │ ├── tables.py # API routes for Table management (Planned)
│ │ │ └── # ... other endpoint files
│ │ └── api.py # Main API router, includes all endpoint routers
│ ├── core/
│ │ ├── **init**.py
│ │ ├── config.py # Application settings and environment variables
│ │ ├── database.py # SQLAlchemy engine, session, Base, TimestampMixin
│ │ ├── security.py # Password hashing, JWT utilities
│ ├── crud/
│ │ ├── **init**.py
│ │ ├── employee.py # CRUD operations for Employee (Implemented)
│ │ ├── menu_item.py # CRUD for Menu Items (Planned)
│ │ ├── order.py # CRUD for Orders (Planned)
│ │ ├── # ... other CRUD files
│ ├── models/
│ │ ├── **init**.py
│ │ ├── employee.py # SQLAlchemy Employee model (Implemented)
│ │ ├── menu_item.py # SQLAlchemy Menu Item model (Planned)
│ │ ├── order.py # SQLAlchemy Order model (Planned)
│ │ ├── order_item.py # SQLAlchemy Order Item model (Planned)
│ │ ├── # ... other SQLAlchemy models
│ ├── schemas/
│ │ ├── **init**.py
│ │ ├── auth.py # Pydantic schemas for authentication
│ │ ├── employee.py # Pydantic schemas for Employee
│ │ ├── mixins.py # Pydantic TimestampMixinSchema
│ │ ├── menu_item.py # Pydantic schemas for Menu Item (Planned)
│ │ ├── order.py # Pydantic schemas for Order (Planned)
│ │ ├── # ... other Pydantic schemas
│ └── main.py # Main FastAPI application entry point
├── alembic/ # Database migrations managed by Alembic
│ ├── versions/
│ └── env.py
│ └── ...
├── .env # Environment variables (local)
├── .env.example # Example environment variables
├── requirements.txt # Python dependencies
└── README.md # This file

Setup and Local Development
Follow these steps to get the project up and running on your local machine.

1. Clone the Repository
   git clone https://github.com/Franckgou/restaurant-pos-system.git
   cd restaurant-pos-system

2. Create a Virtual Environment
   It's highly recommended to use a virtual environment to manage dependencies.

python -m venv venv
source venv/bin/activate # On Windows: .\venv\Scripts\activate

3. Install Dependencies
   pip install -r requirements.txt

4. Configure Environment Variables
   Create a .env file in the project root based on .env.example.

# .env

DATABASE_URL="postgresql://user:password@localhost:5432/your_database_name"
TEST_DATABASE_URL="postgresql://user:password@localhost:5432/your_test_database_name"
SECRET_KEY="your_super_secret_jwt_key_here" # Generate a strong random string
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
REDIS_URL="redis://localhost:6379/0" # If using Redis for caching/queues
ENVIRONMENT="development"

Note: For SECRET_KEY, you can generate a strong one using:

import secrets
print(secrets.token_urlsafe(32))

5. Set Up PostgreSQL Database
   Ensure you have a PostgreSQL server running. Create the databases specified in your .env file (e.g., your_database_name and your_test_database_name).

6. Run Database Migrations (Alembic)
   Initialize Alembic and apply migrations to create your database tables.

# Initialize Alembic (only once per project)

alembic init alembic

# Configure alembic.ini (ensure script_location points to your alembic folder

# and sqlalchemy.url points to your DATABASE_URL from .env)

# Generate your first migration (or subsequent migrations as you add models)

alembic revision --autogenerate -m "create initial tables"

# Apply migrations to your database

alembic upgrade head

Running the Application
To start the FastAPI development server:

uvicorn app.main:app --reload

The API will be accessible at http://127.0.0.1:8000.
The interactive API documentation (Swagger UI) will be available at http://127.0.0.1:8000/docs.
The alternative API documentation (Redoc) will be available at http://127.0.0.1:8000/redoc.

API Endpoints
The API is structured with versioning (e.g., /v1). All endpoints return JSON responses.

Authentication Endpoints (/v1/auth)
POST /v1/auth/login

Description: Authenticates an employee and returns an access token.

Request Body (LoginRequest):

{
"employee_id": "string",
"password": "string"
}

Successful Response (LoginResponse - 200 OK):

{
"access_token": "string",
"token_type": "bearer",
"name": "string",
"role": "waiter | cook | busboy | manager",
"employee_id": "string"
}

POST /v1/auth/change-password

Description: Allows an authenticated user to change their password.

Requires: Valid JWT in Authorization: Bearer <token> header.

Request Body (ChangePassword):

{
"current_password": "string",
"new_password": "string"
}

Successful Response (200 OK):

{
"message": "Password updated successfully!"
}

Employee Management Endpoints (/v1/employees)
POST /v1/employees/

Description: Creates a new employee.

Requires: Manager role, valid JWT.

Request Body (EmployeeCreate):

{
"employee_id": "string",
"name": "string",
"email": "user@example.com",
"is_active": true,
"role": "waiter | cook | busboy | manager",
"password": "string"
}

Successful Response (Employee - 201 Created):

{
"employee_id": "string",
"name": "string",
"email": "user@example.com",
"is_active": true,
"role": "waiter | cook | busboy | manager",
"id": 0,
"last_login": "2023-10-27T00:00:00.000Z",
"login_count": 0,
"created_at": "2023-10-27T00:00:00.000Z",
"updated_at": "2023-10-27T00:00:00.000Z"
}

GET /v1/employees/{employee_id}

Description: Retrieves a single employee's details by their employee_id.

Requires: Manager role OR the employee themselves, valid JWT.

Path Parameters: employee_id (string)

Successful Response (Employee - 200 OK):

# Same as POST response body above

GET /v1/employees/

Description: Retrieves a paginated list of all employees.

Requires: Manager role, valid JWT.

Query Parameters: skip (integer, default 0), limit (integer, default 100)

Successful Response (List of Employee - 200 OK):

[

# Array of Employee objects

]

PUT /v1/employees/{employee_id}

Description: Updates an existing employee's information.

Requires: Manager role, valid JWT.

Path Parameters: employee_id (string)

Request Body (EmployeeUpdate):

{
"name": "string",
"role": "waiter | cook | busboy | manager",
"email": "user@example.com",
"is_active": true,
"password": "string"
}

Successful Response (Employee - 200 OK):

# Same as POST response body above

DELETE /v1/employees/{employee_id}

Description: Soft deletes an employee (sets is_active to False).

Requires: Manager role, valid JWT.

Path Parameters: employee_id (string)

Successful Response (200 OK):

{
"message": "Employee deactivated successfully"
}

Key Features (Planned & Implemented)
Password-Secure Login System: Robust authentication with JWT and Bcrypt. (Implemented)

Role-Based Access Control: Granular permissions for Managers, Waiters, Cooks, and Busboys. (Implemented for Employees)

Employee Management: Full CRUD operations for employee profiles. (Implemented)

Dynamic Floor Chart & Guest Seating: (Planned)

Table Status System: Real-time updates for table availability. (Planned)

Order Management: Add, modify, remove items from orders, seat tracking. (Planned)

Categorical Menu Organization: (Planned)

FIFO Queue for Cooks: Order display and completion tracking. (Planned)

Inventory Tracking: Manual updates, automatic deductions. (Planned)

Sales Analysis: Revenue tracking by item, category, and time. (Planned)

Employee Hours & Payroll Processing: Clock in/out, timecard generation. (Planned)

Future Enhancements
Implementation of remaining CRUD operations for Order, MenuItem, Table, Inventory, Customer, and Payment entities.

Integration with a real-time messaging system (e.g., WebSockets) for live updates (e.g., kitchen display, table status).

Advanced analytics and reporting features.

Containerization with Docker and deployment to cloud platforms.

Comprehensive unit and integration testing.

Contributing
Contributions are welcome! Please follow the standard fork-and-pull-request workflow.

License
This project is licensed under the MIT License. See the LICENSE file for details.
