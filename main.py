"""
Main entry point for the ToDoList application.
Initializes the application layers and starts the command-line interface.
"""
import os
from dotenv import load_dotenv

from storage.in_memory import InMemoryStorage
from core.services import ProjectService
from cli.main import CLI

def main():
    """
    Initializes and runs the application.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Read configuration from environment variables with default fallbacks
    try:
        max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
        max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK_PER_PROJECT", "20"))
    except (ValueError, TypeError):
        print("Error: Invalid configuration values in .env file. Using default values.")
        max_projects = 10
        max_tasks = 20

    # 1. Initialize the Storage layer
    storage = InMemoryStorage()

    # 2. Initialize the Service layer and inject dependencies (storage and config)
    service = ProjectService(
        storage=storage, 
        max_projects=max_projects, 
        max_tasks_per_project=max_tasks
    )

    # 3. Initialize the CLI layer and inject the service
    cli_app = CLI(project_service=service)

    # 4. Start the application
    cli_app.run()

if __name__ == "__main__":
    main()