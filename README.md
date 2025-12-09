# ToDoList Project - Phase 3 (Web API Integration)

**Phase 3** marks the major evolution of the ToDoList application from a Command-Line Interface (CLI) to a robust **RESTful Web API** built with the **FastAPI** framework.

This phase introduces a professional HTTP interface, automatic interactive documentation (Swagger UI), and strict input validation using Pydantic, while maintaining the clean architecture and data persistence established in previous phases.

---

## 🚀 Key Features

* [cite_start]**RESTful API:** Full CRUD operations for Projects and Tasks exposed via standard HTTP methods (GET, POST, PUT, DELETE)[cite: 11, 728].
* [cite_start]**Layered Architecture:** Strict separation of concerns ensuring scalability and maintainability[cite: 14]:
    * **Controllers:** Handle HTTP requests and responses.
    * **Services:** Encapsulate business logic and rules.
    * **Repositories:** Manage direct database interactions.
* [cite_start]**Automatic Documentation:** Interactive API docs generated automatically via **Swagger UI** and **ReDoc**[cite: 442, 1022].
* [cite_start]**Data Validation:** Robust input/output validation using **Pydantic Models**[cite: 632, 1023].
* **Database Persistence:** Reliable data storage using **PostgreSQL** and **SQLAlchemy**.
* [cite_start]**Pagination:** Efficient data retrieval for lists using `skip` and `limit` parameters[cite: 767].
* [cite_start]**Legacy Support:** The CLI tool is preserved for backward compatibility but is now marked as **Deprecated**[cite: 910].

---

## 🏛️ Architecture

The project follows a **Clean Layered Architecture**. The API acts as the new entry point, delegating logic to services, which in turn use repositories to access the database.

```mermaid
graph LR
    Client[Web Browser / Swagger] -->|HTTP Request| API[FastAPI Controllers]
    Legacy[Legacy CLI] -->|Function Calls| Service
    API -->|Pydantic Models| Service[Service Layer]
    Service -->|Business Logic| Repo[Repository Layer]
    Repo -->|SQLAlchemy| DB[(PostgreSQL Database)]