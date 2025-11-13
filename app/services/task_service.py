"""
Contains all business logic related to Task management.
"""
from datetime import date # <-- این import برای کار با تاریخ لازم است
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.exceptions.base import ProjectNotFoundError, TaskNotFoundError
from app.models.task import Task, TaskStatus # <-- این import برای استفاده از TaskStatus لازم است

class TaskService:
    """
    سرویس برای مدیریت منطق بیزینسی تسک‌ها.
    """
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository, max_tasks_per_project: int):
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.max_tasks_per_project = max_tasks_per_project

    def add_task_to_project(self, project_id: int, title: str, description: str, deadline_str: str | None) -> Task:
        project = self.project_repo.get_project_by_id(project_id)
        if not project: 
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        if len(project.tasks) >= self.max_tasks_per_project: 
            raise Exception(f"Cannot add more tasks. Project '{project.name}' has reached the limit.")
        if not title or not title.strip():
            raise ValueError("Task title is mandatory and cannot be empty.")
        if len(title.split()) > 30: 
            raise ValueError("Task title cannot exceed 30 words.")
        if description and len(description.split()) > 150: 
            raise ValueError("Task description cannot exceed 150 words.")
        
        deadline = None
        if deadline_str:
            try: 
                deadline = date.fromisoformat(deadline_str)
            except ValueError: 
                raise ValueError("Invalid deadline format. Use YYYY-MM-DD.")
        
        return self.task_repo.add_task_to_project(
            project=project, 
            title=title.strip(), 
            description=description.strip(), 
            deadline=deadline
        )

    def get_tasks_for_project(self, project_id: int) -> list[Task]:
        if not self.project_repo.get_project_by_id(project_id): 
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        
        return self.task_repo.get_tasks_for_project(project_id)

    def change_task_status(self, project_id: int, task_id: int, new_status_str: str) -> Task:
        try: 
            new_status = TaskStatus(new_status_str.lower())
        except ValueError: 
            raise ValueError(f"'{new_status_str}' is not a valid status. Use 'todo', 'doing', or 'done'.")
        
        task = self.task_repo.get_task_by_id(task_id)
        if not task: 
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
        if task.project_id != project_id:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}.")
            
        task.status = new_status
        return self.task_repo.update_task(task)

    def edit_task(self, project_id: int, task_id: int, new_title: str | None, new_description: str | None, new_deadline_str: str | None) -> Task:
        task = self.task_repo.get_task_by_id(task_id)
        if not task: 
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
        if task.project_id != project_id:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}.")

        if new_title is not None:
            if not new_title or not new_title.strip():
                raise ValueError("New task title is mandatory and cannot be empty.")
            if len(new_title.split()) > 30: 
                raise ValueError("New task title cannot exceed 30 words.")
            task.title = new_title.strip()

        if new_description is not None:
            if len(new_description.split()) > 150: 
                raise ValueError("New task description cannot exceed 150 words.")
            task.description = new_description.strip()

        if new_deadline_str is not None:
            if new_deadline_str.lower() == 'none': 
                task.deadline = None
            else:
                try: 
                    task.deadline = date.fromisoformat(new_deadline_str)
                except ValueError: 
                    raise ValueError("Invalid deadline format. Use YYYY-MM-DD.")
                    
        return self.task_repo.update_task(task)

    def delete_task(self, project_id: int, task_id: int) -> None:
        task = self.task_repo.get_task_by_id(task_id)
        if not task: 
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
        if task.project_id != project_id:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}.")
            
        self.task_repo.delete_task(task)

    # --- متد جا افتاده ---
    def autoclose_overdue_tasks(self) -> int:
        """
        تسک‌های تاریخ‌گذشته را پیدا کرده و وضعیت آن‌ها را به DONE تغییر می‌دهد.
        تعداد تسک‌های بسته شده را برمی‌گرداند.
        """
        # ۱. پیدا کردن تسک‌های دیرشده
        overdue_tasks = self.task_repo.get_overdue_tasks()
        if not overdue_tasks:
            return 0  # هیچ تسکی برای بستن وجود ندارد

        # ۲. تغییر وضعیت همه‌ی آن‌ها
        for task in overdue_tasks:
            task.status = TaskStatus.DONE
        
        # ۳. ذخیره تمام تغییرات در یک تراکنش
        self.task_repo.db.commit()
        
        return len(overdue_tasks)