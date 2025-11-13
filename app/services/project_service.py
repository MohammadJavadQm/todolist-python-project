"""
Contains all business logic related to Project management.
"""
from app.repositories.project_repository import ProjectRepository
from app.exceptions.base import ProjectNotFoundError
from app.models.project import Project

class ProjectService:
    """
    سرویس برای مدیریت منطق بیزینسی پروژه‌ها.
    این لایه هیچ اطلاعی از دیتابیس (SQLAlchemy) ندارد.
    """
    def __init__(self, project_repo: ProjectRepository, max_projects: int):
        self.project_repo = project_repo
        self.max_projects = max_projects

    def create_project(self, name: str, description: str) -> Project:
        """یک پروژه جدید با رعایت قوانین بیزینسی ایجاد می‌کند."""
        
        # قانون ۱: نام الزامی است
        if not name or not name.strip():
            raise ValueError("Project name is mandatory and cannot be empty.")

        # قانون ۲: ولیدیشن تعداد کلمات
        if len(name.split()) > 30: 
            raise ValueError("Project name cannot exceed 30 words.")
        if description and len(description.split()) > 150: 
            raise ValueError("Project description cannot exceed 150 words.")
        
        # قانون ۳: نام نباید تکراری باشد (بررسی توسط سرویس)
        existing_project = self.project_repo.get_project_by_name(name.strip())
        if existing_project:
            raise ValueError(f"A project with the name '{name.strip()}' already exists.")
        
        # قانون ۴: سقف تعداد پروژه‌ها
        if len(self.project_repo.get_all_projects()) >= self.max_projects: 
            raise Exception("Cannot create more projects. The maximum limit has been reached.")
            
        # اگر همه قوانین رعایت شد، به ریپازیتوری دستور ذخیره بده
        return self.project_repo.create_project(name=name.strip(), description=description.strip())

    def edit_project(self, project_id: int, new_name: str | None, new_description: str | None) -> Project:
        """یک پروژه موجود را ویرایش می‌کند."""
        
        # ابتدا پروژه را پیدا کن
        project = self.project_repo.get_project_by_id(project_id)
        if not project: 
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        
        if new_name is not None:
            # قانون ۱: نام الزامی است
            if not new_name or not new_name.strip():
                raise ValueError("New project name is mandatory and cannot be empty.")
            # قانون ۲: ولیدیشن تعداد کلمات
            if len(new_name.split()) > 30: 
                raise ValueError("New project name cannot exceed 30 words.")
            # قانون ۳: بررسی تکراری بودن نام جدید
            existing_project = self.project_repo.get_project_by_name(new_name.strip())
            if existing_project and existing_project.id != project_id: 
                raise ValueError(f"Another project with the name '{new_name.strip()}' already exists.")
            project.name = new_name.strip()

        if new_description is not None:
            # قانون ۲: ولیدیشن تعداد کلمات
            if len(new_description.split()) > 150: 
                raise ValueError("New project description cannot exceed 150 words.")
            project.description = new_description.strip()
        
        # اگر همه چیز اوکی بود، به ریپازیتوری دستور آپدیت بده
        return self.project_repo.update_project(project)

    def delete_project(self, project_id: int) -> None:
        """یک پروژه را حذف می‌کند."""
        project = self.project_repo.get_project_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        
        # Cascade delete در دیتابیس و SQLAlchemy تنظیم شده،
        # پس ریپازیتوری فقط باید پروژه را حذف کند.
        self.project_repo.delete_project(project)

    def get_all_projects(self) -> list[Project]:
        """تمام پروژه‌ها را برمی‌گرداند."""
        return self.project_repo.get_all_projects()