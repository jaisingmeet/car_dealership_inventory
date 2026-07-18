# Car Dealership Inventory System

A robust, production-ready Full-Stack Car Dealership Inventory System built following strict **Test-Driven Development (TDD)** principles. The application includes role-based access control (RBAC), secure JWT authentication, advanced search metrics, and an automated transactional inventory flow.

## 🚀 Tech Stack

- **Backend:** Python 3.13, FastAPI, SQLAlchemy
- **Database:** SQLite (Persistent relational database mapping)
- **Testing Suite:** Pytest with custom transaction isolation fixtures
- **Frontend (In Progress):** React, Tailwind CSS, HTML5

---

## 🛠️ Backend Setup & Installation

### Prerequisite
Make sure you have Python 3.13+ installed on your machine.

1. **Navigate to the workspace:**
   ```bash
   cd backend
## ⚠️ Design Decisions & Current Limitations

- **Role-Based Access Control (RBAC):** For the scope of this Kata, user privilege validation (`is_admin`) is simplified via a username pattern match during test executions. In a production environment, this would be refactored into a dedicated database column managed through a secure seeding script or administrative console.
- **Environment Management:** The `SECRET_KEY` is currently static for quick testing compilation. Production deployments will pull this directly via `os.getenv("SECRET_KEY")` wrapped inside a protected environment wrapper.