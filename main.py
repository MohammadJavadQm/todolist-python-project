"""
نقطه ورود اصلی اپلیکیشن ToDoList.
این فایل مسئول راه‌اندازی لایه‌ها و تزریق وابستگی‌ها است.
"""
import os
from dotenv import load_dotenv
from app.db.session import SessionLocal
from app.cli.main import CLI
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService

def main():
    """
    راه‌اندازی و اجرای اپلیکیشن.
    اینجا "Composition Root" ما است.
    """
    # بارگذاری متغیرهای محیطی از .env
    load_dotenv()
    try:
        max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
        max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK_PER_PROJECT", "20"))
    except (ValueError, TypeError):
        print("Error: Invalid configuration values in .env file. Using default values.")
        max_projects = 10
        max_tasks = 20

    # 1. ساخت یک سشن دیتابیس
    # ما یک سشن در طول عمر برنامه می‌سازیم
    db = SessionLocal()

    try:
        # 2. راه‌اندازی لایه Repository (با تزریق سشن)
        project_repo = ProjectRepository(db=db)
        task_repo = TaskRepository(db=db)

        # 3. راه‌اندازی لایه Service (با تزریق ریپازیتوری و تنظیمات)
        project_service = ProjectService(
            project_repo=project_repo,
            max_projects=max_projects
        )
        task_service = TaskService(
            task_repo=task_repo,
            project_repo=project_repo,  # TaskService به هر دو ریپازیتوری نیاز دارد
            max_tasks_per_project=max_tasks
        )

        # 4. راه‌اندازی لایه CLI (با تزریق سرویس‌ها)
        cli_app = CLI(project_service=project_service, task_service=task_service)

        # 5. اجرای برنامه
        cli_app.run()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # 6. اطمینان از بسته شدن سشن دیتابیس در هر حال
        print("Closing database session.")
        db.close()

if __name__ == "__main__":
    main()