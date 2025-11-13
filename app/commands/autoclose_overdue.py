"""
اسکریپت مستقل برای بستن خودکار تسک‌های تاریخ‌گذشته.
این اسکریپت باید به صورت مستقل از CLI اصلی قابل اجرا باشد.
"""
import os
import sys 

# --- شروع اصلاحیه ---
# این یک "ترفند مسیر" است تا اسکریپت بتواند پکیج 'app' را پیدا کند
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)
# --- پایان اصلاحیه ---

from dotenv import load_dotenv
from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService

def run_autoclose_overdue():
    """
    تسک‌های تاریخ‌گذشته را پیدا کرده و می‌بندد.
    این تابع تمام وابستگی‌های مورد نیاز خود را می‌سازد.
    """
    
    # بارگذاری متغیرهای محیطی
    # .env باید در پوشه ریشه (PROJECT_ROOT) باشد
    load_dotenv(os.path.join(PROJECT_ROOT, '.env'))
    try:
        max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK_PER_PROJECT", "20"))
    except (ValueError, TypeError):
        max_tasks = 20

    # ۱. ساخت سشن دیتابیس
    db = SessionLocal()
    
    try:
        # ۲. راه‌اندازی لایه‌ها
        project_repo = ProjectRepository(db=db)
        task_repo = TaskRepository(db=db)
        task_service = TaskService(
            task_repo=task_repo,
            project_repo=project_repo,
            max_tasks_per_project=max_tasks
        )

        # ۳. اجرای سرویس
        closed_count = task_service.autoclose_overdue_tasks()
        
        if closed_count > 0:
            print(f"✅ Success: Auto-closed {closed_count} overdue task(s).")
        else:
            print("ℹ️ Info: No overdue tasks found to close.")
            
    except Exception as e:
        print(f"❌ Error during auto-close job: {e}")
    finally:
        # ۴. بستن سشن
        db.close()

if __name__ == "__main__":
    # این امکان را می‌دهد که فایل را مستقیماً اجرا کنیم
    # poetry run python app/commands/autoclose_overdue.py
    print("Running job directly: Auto-closing overdue tasks...")
    run_autoclose_overdue()