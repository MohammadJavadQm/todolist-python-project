"""
زمان‌بند (Scheduler) اصلی برنامه.
این اسکریپت به صورت دائم اجرا می‌شود و تسک‌های زمان‌بندی شده را
بر اساس برنامه اجرا می‌کند.
"""
import schedule
import time
import sys
import os

# --- شروع اصلاحیه ---
# این یک "ترفند مسیر" است تا اسکریپت بتواند پکیج 'app' را پیدا کند
# آدرس پوشه ریشه پروژه (دو مرحله بالاتر) را به مسیر پایتون اضافه می‌کند
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)
# --- پایان اصلاحیه ---

# حالا این import به درستی کار خواهد کرد
from app.commands.autoclose_overdue import run_autoclose_overdue

def job():
    """تابعی که قرار است به صورت زمان‌بندی شده اجرا شود."""
    print(f"\n[{time.ctime()}] Running scheduled job: Auto-closing overdue tasks...")
    try:
        run_autoclose_overdue()
    except Exception as e:
        print(f"Error in scheduled job: {e}")

def main():
    print("Scheduler started. Running job every 15 minutes...")
    
    # تنظیم زمان‌بندی
    # (برای تست می‌توانید 15.minutes را به 1.minutes تغییر دهید)
    schedule.every(15).minutes.do(job)

    # اجرای فوری کار برای اولین بار
    print(f"[{time.ctime()}] Running job for the first time...")
    job()

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()