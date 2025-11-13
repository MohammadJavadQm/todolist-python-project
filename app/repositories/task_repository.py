from sqlalchemy.orm import Session
from app.models.task import Task, TaskStatus
from app.models.project import Project
from datetime import date

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_task_by_id(self, task_id: int) -> Task | None:
        """دریافت یک تسک بر اساس شناسه."""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_tasks_for_project(self, project_id: int) -> list[Task]:
        """دریافت لیست تمام تسک‌های یک پروژه."""
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def add_task_to_project(self, project: Project, title: str, description: str, deadline: date | None) -> Task:
        """ایجاد یک تسک جدید برای یک پروژه مشخص."""
        db_task = Task(
            title=title,
            description=description,
            deadline=deadline,
            project_id=project.id  # اتصال تسک به پروژه
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete_task(self, task: Task) -> None:
        """حذف یک تسک."""
        self.db.delete(task)
        self.db.commit()

    def update_task(self, task: Task) -> Task:
        """به‌روزرسانی یک تسک."""
        self.db.commit()
        self.db.refresh(task)
        return task