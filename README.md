# ToDoList CLI Application - Phase 1

This project is a command-line interface (CLI) application for managing tasks and projects, developed as the first phase of a comprehensive software engineering project. The primary focus of this phase has been on implementing a **Clean Architecture**, adhering to **Object-Oriented Programming (OOP)** principles, and following **professional coding and workflow conventions**.

-----

## 🚀 Key Features

  * **Full Project Management:**
      * Create a new project (`create-project`)
      * Edit a project's name and description (`edit-project`)
      * Delete a project along with all its tasks (Cascade Delete) (`delete-project`)
      * Display a list of all projects (`list-projects`)
  * **Complete Task Management:**
      * Add a new task to a specific project (`add-task`)
      * Edit task details (title, description, deadline) (`edit-task`)
      * Change a task's status (todo, doing, done) (`change-task-status`)
      * Delete a task (`delete-task`)
      * Display all tasks within a specific project (`list-tasks`)
  * **External Configuration:** Project and task limits are managed via an `.env` file to decouple configuration from the codebase.
  * **User Interface:** All user interactions are handled through a simple and intuitive Command-Line Interface (CLI).
  * **Storage:** In this phase, all data is stored temporarily in-memory. The state is reset every time the application is relaunched.

-----

## 🏛️ Architecture and Design

This project is designed following the **Separation of Concerns** principle with a clean, three-layer architecture. This design significantly enhances the code's maintainability, scalability, and testability.

```
+--------------------------+
|      CLI Layer           |  (Presentation Layer - cli/main.py)
|      (User Interface)    |  Handles user interaction
+-----------+--------------+
            |
            v
+-----------+--------------+
|      Core Layer          |  (Business Logic Layer - core/services.py)
|      (Business Logic)    |  The "brain" of the application, contains all business rules
+-----------+--------------+
            |
            v
+-----------+--------------+
|      Storage Layer       |  (Data Access Layer - storage/in_memory.py)
|      (Data Access)       |  Responsible for storing and retrieving data
+--------------------------+
```

Dependencies are managed using the **Dependency Injection** pattern to ensure that layers remain decoupled and independent.

-----

## 🛠️ Tools & Technologies

  * **Language:** Python 3.10+
  * **Dependency & Environment Management:** Poetry
  * **Version Control:** Git & GitHub
  * **Git Workflow:** Git Flow (utilizing `main`, `develop`, and `feature/*` branches)

-----

## ⚙️ Setup and Installation

Follow these steps to set up the project on your local machine.

**Prerequisites:**

  * [Git](https://git-scm.com/)
  * [Python 3.10](https://www.python.org/) or newer
  * [Poetry](https://python-poetry.org/)

**Installation Steps:**

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/MohammadJavadQm/todolist-python-project.git
    cd todolist-python-project
    ```

2.  **Install dependencies:**
    Poetry will automatically create a virtual environment and install the required packages.

    ```bash
    poetry install
    ```

3.  **Set up the configuration file:**
    Copy the `.env.example` file to `.env` and modify the values as needed.

    ```bash
    # For Windows
    copy .env.example .env

    # For macOS/Linux
    cp .env.example .env
    ```

-----

## ▶️ How to Run

To run the application, execute the following command from the project's root directory:

```bash
poetry run python main.py
```

-----

## 📋 Available Commands

Once the application is running, you can use the following commands to interact with it:

| Command                | Description                                                 |
| ---------------------- | ----------------------------------------------------------- |
| `help`                 | Displays a list of all available commands.                  |
| `exit`                 | Exits the application.                                      |
| **--- Project Management ---** |                                                             |
| `create-project`       | Creates a new project.                                      |
| `list-projects`        | Lists all existing projects.                                |
| `edit-project`         | Edits the name and description of an existing project.      |
| `delete-project`       | Deletes a project and all of its associated tasks.          |
| **--- Task Management ---** |                                                             |
| `add-task`             | Adds a new task to a project.                               |
| `list-tasks`           | Lists all tasks for a specific project.                     |
| `change-task-status`   | Changes a task's status to `todo`, `doing`, or `done`.      |
| `edit-task`            | Edits a task's details (title, description, deadline).      |
| `delete-task`          | Deletes a specific task.                                    |