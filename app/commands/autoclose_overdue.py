"""
اسکریپت مستقل برای بستن خودکار تسک‌های تاریخ‌گذشته.
نسخه هماهنگ شده با فاز ۳ (استفاده از Repository).
"""
import os
import sys 

# --- ترفند مسیر ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)
# ------------------

from dotenv import load_dotenv
from app.db.session import SessionLocal
from app.repositories.task_repository import TaskRepository

def run_autoclose_overdue():
    # 1. بارگذاری متغیرها
    load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

    # 2. ساخت سشن دیتابیس
    db = SessionLocal()
    
    try:
        # 3. استفاده از Repository
        # در فاز ۳، منطق بستن تسک‌ها را داخل TaskRepository متد autoclose_overdue_tasks گذاشتیم
        task_repo = TaskRepository(db)
        
        print("🔍 Checking for overdue tasks...")
        closed_count = task_repo.autoclose_overdue_tasks()
        
        if closed_count > 0:
            print(f"✅ Success: Auto-closed {closed_count} overdue task(s).")
        else:
            print("ℹ️ Info: No overdue tasks found.")
            
    except Exception as e:
        print(f"❌ Error during auto-close job: {e}")
    finally:
        # 4. بستن اجباری سشن
        db.close()

if __name__ == "__main__":
    run_autoclose_overdue()