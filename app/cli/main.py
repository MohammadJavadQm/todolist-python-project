"""
The command-line interface for the ToDoList application.
Handles user input and orchestrates calls to the appropriate service layers.
"""
# Import both service classes for type hinting
from app.services.project_service import ProjectService
from app.services.task_service import TaskService

class CLI:
    """Manages all command-line interactions."""
    # The constructor now accepts two separate services
    def __init__(self, project_service: ProjectService, task_service: TaskService):
        self._project_service = project_service
        self._task_service = task_service
        self.commands = {
            "create-project": self.create_project,
            "list-projects": self.list_projects,
            "edit-project": self.edit_project,
            "delete-project": self.delete_project,
            "add-task": self.add_task,
            "list-tasks": self.list_tasks,
            "change-task-status": self.change_task_status,
            "edit-task": self.edit_task,
            "delete-task": self.delete_task,
            "help": self.show_help,
            "exit": self.exit_app,
        }

    def show_help(self):
        """Displays all available commands to the user."""
        print("\nAvailable commands:")
        for command in self.commands:
            print(f"  - {command}")
        print()

    def exit_app(self):
        """Exits the application."""
        print("Exiting the application. Goodbye!")
        return True

    # --- Project Methods ---

    def create_project(self):
        """Handles the 'create-project' command."""
        try:
            name = input("Enter project name: ")
            desc = input("Enter project description: ")
            # Use the dedicated project service
            project = self._project_service.create_project(name, desc)
            print(f"---\n✅ Success! Project '{project.name}' created with ID {project.id}.\n---")
        except (ValueError, Exception) as e:
            print(f"---\n❌ Error: {e}\n---")

    def list_projects(self):
        """Handles the 'list-projects' command, now including descriptions."""
        projects = self._project_service.get_all_projects()
        if not projects:
            print("---\nℹ️ No projects found. Use 'create-project' to add one.\n---")
            return
        
        print("\n--- Projects ---")
        for proj in projects:
            # CORRECTED: Now displays the project description as required.
            print(f"  ID: {proj.id}, Name: {proj.name}\n    Description: {proj.description} ({len(proj.tasks)} tasks)")
        print("----------------\n")

    def edit_project(self):
        """Handles the 'edit-project' command."""
        try:
            project_id = int(input("Enter the Project ID to edit: "))
            print("Enter new values. Press Enter to keep the current value.")
            new_name = input("New project name: ") or None
            new_desc = input("New project description: ") or None
            # Use the dedicated project service
            project = self._project_service.edit_project(project_id, new_name, new_desc)
            print(f"---\n✅ Success! Project {project.id} has been updated.\n---")
        except (ValueError, Exception) as e:
            print(f"---\n❌ Error: {e}\n---")

    def delete_project(self):
        """Handles the 'delete-project' command."""
        try:
            project_id = int(input("Enter the Project ID to delete: "))
            confirm = input(f"Are you sure you want to delete project {project_id} and all its tasks? (yes/no): ").lower()
            if confirm == 'yes':
                # Use the dedicated project service
                self._project_service.delete_project(project_id)
                print(f"---\n✅ Success! Project {project_id} has been deleted.\n---")
            else:
                print("---\nℹ️ Deletion cancelled.\n---")
        except (ValueError, Exception) as e:
            print(f"---\n❌ Error: {e}\n---")

    # --- Task Methods ---

    def add_task(self):
        """Handles the 'add-task' command."""
        try:
            project_id = int(input("Enter the Project ID to add the task to: "))
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            deadline = input("Enter deadline (YYYY-MM-DD, optional): ")
            # Use the dedicated task service
            task = self._task_service.add_task_to_project(project_id, title, description, deadline or None)
            print(f"---\n✅ Success! Task '{task.title}' added to project ID {project_id}.\n---")
        except (ValueError, Exception) as e:
            print(f"---\n❌ Error: {e}\n---")

    def list_tasks(self):
        """Handles the 'list-tasks' command."""
        try:
            project_id = int(input("Enter the Project ID to list tasks from: "))
            # Use the dedicated task service
            tasks = self._task_service.get_tasks_for_project(project_id)
            if not tasks:
                print(f"---\nℹ️ No tasks found for project ID {project_id}.\n---")
                return
            
            print(f"\n--- Tasks in Project ID {project_id} ---")
            for task in tasks:
                deadline_str = f", Deadline: {task.deadline}" if task.deadline else ""
                print(f"  ID: {task.id}, Status: {task.status.value.upper()}, Title: {task.title}{deadline_str}")
            print("--------------------------------\n")
        except (ValueError, Exception) as e:
            print(f"---\n❌ Error: {e}\n---")
    
    def change_task_status(self):
        """Handles the 'change-task-status' command."""
        try:
            project_id = int(input("Enter the Project ID: "))
            task_id = int(input("Enter the Task ID: "))
            new_status = input("Enter the new status (todo, doing, done): ")
            # Use the dedicated task service
            task = self._task_service.change_task_status(project_id, task_id, new_status)
            print(f"---\n✅ Success! Task {task.id} status changed to '{task.status.value.upper()}'.\n---")
        except (ValueError, Exception) as e:
            print(f"---\n❌ Error: {e}\n---")
    
    def edit_task(self):
        """Handles the 'edit-task' command."""
        try:
            project_id = int(input("Enter the Project ID of the task: "))
            task_id = int(input("Enter the Task ID to edit: "))
            
            print("Enter new values. Press Enter to keep the current value.")
            new_title = input("New title: ") or None
            new_desc = input("New description: ") or None
            new_deadline = input("New deadline (YYYY-MM-DD or 'none' to remove): ") or None
            # Use the dedicated task service
            task = self._task_service.edit_task(project_id, task_id, new_title, new_desc, new_deadline)
            print(f"---\n✅ Success! Task {task.id} has been updated.\n---")
        except (ValueError, Exception) as e:
            print(f"---\n❌ Error: {e}\n---")

    def delete_task(self):
        """Handles the 'delete-task' command."""
        try:
            project_id = int(input("Enter the Project ID of the task: "))
            task_id = int(input("Enter the Task ID to delete: "))
            # Use the dedicated task service
            self._task_service.delete_task(project_id, task_id)
            print(f"---\n✅ Success! Task {task_id} from project {project_id} has been deleted.\n---")
        except (ValueError, Exception) as e:
            print(f"---\n❌ Error: {e}\n---")

    def run(self):
        """Starts the main loop of the CLI."""
        print("--- ToDoList Application ---")
        self.show_help()
        while True:
            command_input = input("> Enter a command: ").lower().strip()
            command_func = self.commands.get(command_input)
            if command_func:
                if command_func():
                    break
            else:
                print("Unknown command. Type 'help' to see available commands.")