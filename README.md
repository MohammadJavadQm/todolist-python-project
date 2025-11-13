ToDoList Project - Phase 2 (RDB Integration)

This project is a command-line interface (CLI) application for managing tasks and projects. This second phase evolves the application from its initial In-Memory state (Phase 1) into a persistent application using a Clean Layered Architecture, the Repository Pattern, and a PostgreSQL database.

🚀 Key Features

Full Project Management: Create, edit, delete (with cascade), and list projects.

Complete Task Management: Add, edit, delete, change status (todo, doing, done), and list tasks.

Data Persistence: All data is now stored in a real PostgreSQL database, ensuring data is saved between sessions.

Automatic Task Closing: A background scheduler automatically finds and closes overdue tasks by setting their status to DONE.

External Configuration: All settings (including database credentials and limits) are managed via an .env file.

User Interface: All user interactions are handled through the familiar CLI from Phase 1.

🏛️ Architecture and Design (Phase 2)

In this phase, the project was completely refactored to follow the principles of Separation of Concerns (SoC) and Dependency Injection (DI). All application logic now resides within the app/ package.

The new architecture is based on the Repository Pattern:

+--------------------------+
|   CLI (app/cli)          |  (Presentation Layer)
|   (User Interface)       |  Handles user interaction
+-----------+--------------+
            |
            v
+-----------+--------------+
|   Services (app/services)|  (Business Logic Layer)
|   (Business Logic)       |  The "brain" - contains all business rules
+-----------+--------------+
            |
            v
+-----------+--------------+
|   Repositories (app/repo)|  (Data Access Layer)
|   (Repository Pattern)   |  Interface between logic and database
+-----------+--------------+
            |
            v
+-----------+--------------+
|   Models / DB (app/models)|  (Data Layer)
|   (SQLAlchemy ORM)       |  Defines tables and connects to PostgreSQL
+--------------------------+


app/commands: Contains standalone scripts that can be run on a schedule (like autoclose_overdue.py).

🛠️ Tools & Technologies

Language: Python 3.10+

Dependency Management: Poetry

Version Control: Git & GitHub (Git Flow)

Database: PostgreSQL (Running on Docker)

Containerization: Docker Desktop

ORM: SQLAlchemy (For modeling and interacting with the DB)

Database Migrations: Alembic (For creating and updating tables)

Task Scheduling: schedule (For running periodic background jobs)

⚙️ Setup and Installation

Follow these steps to set up the project on your local machine.

Prerequisites:

Git

Python 3.10 or newer

Poetry

Docker Desktop (must be running)

Installation Steps:

Clone the repository:

git clone [https://github.com/MohammadJavadQm/todolist-python-project.git](https://github.com/MohammadJavadQm/todolist-python-project.git)
cd todolist-python-project


Install dependencies:
Poetry will automatically create a virtual environment and install all packages (like sqlalchemy, psycopg2-binary, alembic, and schedule).

poetry install


Set up the configuration file:
Copy .env.example to .env. The values for DB_USER, DB_PASSWORD, and DB_NAME must match what you will set in the Docker command.

# For Windows
copy .env.example .env


Run the PostgreSQL Database with Docker:
Execute the following command in your terminal to run a database container in the background:

docker run --name todolist-db -e POSTGRES_USER=parsa -e POSTGRES_PASSWORD=secret123 -e POSTGRES_DB=mydb -p 5432:5432 -d postgres


(Note: The values parsa, secret123, and mydb must match your .env file).

Run Database Migrations:
This command creates the projects and tasks tables in your new empty database:

poetry run alembic upgrade head


▶️ How to Run

The Phase 2 project has two executable parts that should be run simultaneously (in two separate terminals):

1. Run the Main Application (CLI)

In your first terminal, for interacting with the app:

poetry run python main.py


2. Run the Scheduler

In your second terminal, to automatically close overdue tasks:

poetry run python app/commands/scheduler.py


📋 Available Commands

The CLI commands remain the same as in Phase 1:
| Command | Description |
| :--- | :--- |
| help | Displays a list of all available commands. |
| exit | Exits the application. |
| --- Project Management --- | |
| create-project | Creates a new project. |
| list-projects | Lists all existing projects. |
| edit-project | Edits the name and description of an existing project. |
| delete-project | Deletes a project and all of its associated tasks. |
| --- Task Management --- | |
| add-task | Adds a new task to a project. |
| list-tasks | Lists all tasks for a specific project. |
| change-task-status| Changes a task's status to todo, doing, or done. |
| edit-task | Edits a task's details (title, description, deadline). |
| delete-task | Deletes a specific task. |

🔮 Future Plans (Phase 3)

Develop a REST API using the FastAPI framework on top of the current service layer.

Write Automated Tests (Unit Tests) for the Service and Repository layers.