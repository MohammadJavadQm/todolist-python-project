from sqlalchemy.orm import Session
from app.models.project import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_project_by_id(self, project_id: int) -> Project | None:
        """دریافت یک پروژه بر اساس شناسه."""
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_project_by_name(self, name: str) -> Project | None:
        """دریافت یک پروژه بر اساس نام."""
        return self.db.query(Project).filter(Project.name == name).first()

    def get_all_projects(self, skip: int = 0, limit: int = 100) -> list[Project]:
        """
        دریافت لیست پروژه‌ها با قابلیت صفحه‌بندی.
        اصلاح شده برای دریافت skip و limit.
        """
        return self.db.query(Project).offset(skip).limit(limit).all()

    def create_project(self, name: str, description: str) -> Project:
        """ایجاد یک پروژه جدید."""
        db_project = Project(name=name, description=description)
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def delete_project(self, project: Project) -> None:
        """حذف یک پروژه."""
        self.db.delete(project)
        self.db.commit()

    def update_project(self, project: Project) -> Project:
        """به‌روزرسانی یک پروژه."""
        self.db.commit()
        self.db.refresh(project)
        return project