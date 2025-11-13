# File: main.py

import os
from dotenv import load_dotenv

from storage.in_memory import InMemoryStorage
# Imports are updated to the new structure
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.cli.main import CLI

def main():
    """Initializes and runs the application."""
    load_dotenv()

    try:
        max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
        max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK_PER_PROJECT", "20"))
    except (ValueError, TypeError):
        print("Error: Invalid configuration values in .env file. Using default values.")
        max_projects = 10
        max_tasks = 20

    # 1. Initialize Storage
    storage = InMemoryStorage()

    # 2. Initialize BOTH services and inject dependencies
    project_service = ProjectService(storage=storage, max_projects=max_projects)
    task_service = TaskService(storage=storage, max_tasks_per_project=max_tasks)

    # 3. Initialize the CLI and inject BOTH services
    cli_app = CLI(project_service=project_service, task_service=task_service)

    # 4. Start the application
    cli_app.run()

if __name__ == "__main__":
    main()