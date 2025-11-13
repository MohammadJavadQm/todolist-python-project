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

    def get_all_projects(self) -> list[Project]:
        """دریافت لیست تمام پروژه‌ها."""
        return self.db.query(Project).all()

    def create_project(self, name: str, description: str) -> Project:
        """ایجاد یک پروژه جدید."""
        # ساخت آبجکت مدل
        db_project = Project(name=name, description=description)
        # افزودن به سشن (آماده‌سازی برای ذخیره)
        self.db.add(db_project)
        # ذخیره نهایی در دیتابیس
        self.db.commit()
        # رفرش کردن آبجکت تا ID دیتابیس را دریافت کند
        self.db.refresh(db_project)
        return db_project

    def delete_project(self, project: Project) -> None:
        """حذف یک پروژه."""
        self.db.delete(project)
        self.db.commit()

    def update_project(self, project: Project) -> Project:
        """به‌روزرسانی یک پروژه."""
        # SQLAlchemy به طور خودکار تغییرات روی آبجکت project را ردیابی می‌کند
        # فقط کافیست کامیت کنیم تا ذخیره شود.
        self.db.commit()
        self.db.refresh(project)
        return project