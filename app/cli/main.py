"""
لایه رابط خط فرمان (CLI) اپلیکیشن.
این لایه با استفاده از سرویس‌های جدید و مدل‌های Pydantic بازنویسی شده است.
"""
import sys
from datetime import datetime, date

# اتصال به دیتابیس
from app.db.session import SessionLocal

# سرویس‌ها (به صورت ماژول ایمپورت می‌شوند)
from app.services import project_service, task_service

# مدل‌های درخواست (برای ارسال به سرویس)
from app.api.controller_schemas.requests.project_request_schema import ProjectCreateRequest, ProjectUpdateRequest
from app.api.controller_schemas.requests.task_request_schema import TaskCreateRequest, TaskUpdateRequest

class CLI:
    """مدیریت تمام تعاملات خط فرمان."""
    
    def __init__(self):
        # سرویس‌ها functional هستند و نیاز به اینستنس ندارند
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

    def get_db(self):
        """یک سشن دیتابیس می‌سازد."""
        return SessionLocal()

    def show_help(self):
        """نمایش تمام دستورات موجود."""
        print("\nAvailable commands:")
        for command in self.commands:
            print(f"  - {command}")
        print()

    def exit_app(self):
        """خروج از اپلیکیشن."""
        return True # سیگنال خروج

    
    def create_project(self):
        try:
            name = input("Enter project name: ")
            desc = input("Enter project description (optional): ") or None
            
            # 1. ساخت مدل Pydantic
            request = ProjectCreateRequest(name=name, description=desc)
            
            # 2. باز کردن سشن دیتابیس و فراخوانی سرویس
            with self.get_db() as db:
                project = project_service.create_project(db, request)
                print(f"---\n✅ Success! Project '{project.name}' created with ID {project.id}.\n---")
                
        except Exception as e:
            print(f"---\n❌ Error: {e}\n---")

    def list_projects(self):
        try:
            with self.get_db() as db:
                # دریافت همه پروژه‌ها (بدون صفحه‌بندی در CLI پیش‌فرض ۱۰۰ تا می‌گیریم)
                projects = project_service.get_projects(db, skip=0, limit=100)
                
                if not projects:
                    print("---\nℹ️ No projects found. Use 'create-project' to add one.\n---")
                    return
                
                print("\n--- Projects ---")
                for proj in projects:
                    print(f"  ID: {proj.id}, Name: {proj.name}")
                    print(f"    Description: {proj.description or 'N/A'}")

                print("----------------\n")
        except Exception as e:
            print(f"---\n❌ Error: {e}\n---")

    def edit_project(self):
        try:
            project_id = int(input("Enter the Project ID to edit: "))
            print("Enter new values. Press Enter to keep the current value.")
            new_name = input("New project name: ") or None
            new_desc = input("New project description: ") or None
            
            request = ProjectUpdateRequest(name=new_name, description=new_desc)
            
            with self.get_db() as db:
                project = project_service.update_project(db, project_id, request)
                if project:
                    print(f"---\n✅ Success! Project {project.id} has been updated.\n---")
                else:
                    print("❌ Project not found.")
        except Exception as e:
            print(f"---\n❌ Error: {e}\n---")

    def delete_project(self):
        try:
            project_id = int(input("Enter the Project ID to delete: "))
            confirm = input(f"Are you sure? (yes/no): ").lower()
            if confirm == 'yes':
                with self.get_db() as db:
                    success = project_service.delete_project(db, project_id)
                    if success:
                        print(f"---\n✅ Success! Project {project_id} deleted.\n---")
                    else:
                        print("❌ Project not found.")
            else:
                print("Cancelled.")
        except Exception as e:
            print(f"---\n❌ Error: {e}\n---")

    # --- متدهای تسک ---
    def add_task(self):
        try:
            project_id = int(input("Enter Project ID: "))
            title = input("Enter task title: ")
            desc = input("Enter description (optional): ") or None
            due_date_str = input("Enter deadline (YYYY-MM-DD, optional): ") or None
            
            due_date = None
            if due_date_str:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

            request = TaskCreateRequest(
                project_id=project_id,
                title=title,
                description=desc,
                due_date=due_date
            )
            
            with self.get_db() as db:
                task = task_service.create_task(db, request)
                print(f"---\n✅ Success! Task '{task.title}' added.\n---")
        except Exception as e:
            print(f"---\n❌ Error: {e}\n---")

    def list_tasks(self):
        try:
            # نکته: سرویس get_tasks همه تسک‌ها را برمی‌گرداند
            project_id_input = input("Enter Project ID to filter (or press Enter for all): ")
            
            with self.get_db() as db:
                if project_id_input:
                    # روش صحیح: گرفتن پروژه و نمایش تسک‌هایش
                    proj = project_service.get_project(db, int(project_id_input))
                    if not proj:
                        print("❌ Project not found.")
                        return
                    tasks = proj.tasks # استفاده از Relationship دیتابیس
                    print(f"\n--- Tasks for Project {proj.name} ---")
                else:
                    tasks = task_service.get_tasks(db, limit=100)
                    print("\n--- All Tasks ---")

                for task in tasks:
                    status = task.status.value if hasattr(task.status, 'value') else task.status
                    print(f"  ID: {task.id} | Status: {status} | Title: {task.title}")
                    if task.deadline:
                        print(f"    Deadline: {task.deadline}")
                print("-----------------\n")
                
        except Exception as e:
            print(f"---\n❌ Error: {e}\n---")

    def change_task_status(self):
        try:
            task_id = int(input("Enter Task ID: "))
            new_status = input("Enter new status (todo, doing, done): ").lower()
            
            request = TaskUpdateRequest(status=new_status)
            
            with self.get_db() as db:
                task = task_service.update_task(db, task_id, request)
                if task:
                    print(f"---\n✅ Success! Status changed to '{new_status}'.\n---")
                else:
                    print("❌ Task not found.")
        except Exception as e:
            print(f"---\n❌ Error: {e}\n---")

    def edit_task(self):
        try:
            task_id = int(input("Enter Task ID to edit: "))
            print("Enter new values (Enter to skip):")
            title = input("New title: ") or None
            desc = input("New description: ") or None
            
            request = TaskUpdateRequest(title=title, description=desc)
            
            with self.get_db() as db:
                task = task_service.update_task(db, task_id, request)
                if task:
                    print(f"---\n✅ Success! Task updated.\n---")
                else:
                    print("❌ Task not found.")
        except Exception as e:
            print(f"---\n❌ Error: {e}\n---")

    def delete_task(self):
        try:
            task_id = int(input("Enter Task ID to delete: "))
            confirm = input("Are you sure? (yes/no): ").lower()
            
            if confirm == 'yes':
                with self.get_db() as db:
                    success = task_service.delete_task(db, task_id)
                    if success:
                        print(f"---\n✅ Success! Task {task_id} deleted.\n---")
                    else:
                        print("❌ Task not found.")
            else:
                print("Cancelled.")
        except Exception as e:
            print(f"---\n❌ Error: {e}\n---")

    def run(self):
        """حلقه اصلی اجرای برنامه."""
        print("\n" + "!" * 80)
        print("WARNING: CLI interface is deprecated and will be removed in the next release.")
        print("Please use the FastAPI Web Interface instead.")
        print("!" * 80 + "\n")
        # ---------------------------

        print("--- ToDoList CLI (Phase 3 Migration Mode) ---")
        self.show_help()
        while True:
            try:
                command_input = input("> Enter a command: ").lower().strip()
                if not command_input:
                    continue
                    
                command_func = self.commands.get(command_input)
                
                if command_func:
                    if command_func(): # اگر exit_app بود
                        break
                else:
                    print("Unknown command. Type 'help' to see available commands.")
            except KeyboardInterrupt:
                print("\nExiting application...")
                break
            except Exception as e:
                print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    cli = CLI()
    cli.run()