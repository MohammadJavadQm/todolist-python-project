"""
زمان‌بند (Scheduler) اصلی برنامه.
این اسکریپت همیشه در حال اجراست و اسکریپت autoclose را صدا می‌زند.
"""
import schedule
import time
import sys
import os

# --- ترفند مسیر ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
sys.path.append(PROJECT_ROOT)
# ------------------

# حالا که مسیر درست شد، می‌توانیم فانکشن را ایمپورت کنیم
from app.commands.autoclose_overdue import run_autoclose_overdue

def job():
    """تابعی که قرار است به صورت زمان‌بندی شده اجرا شود."""
    print(f"\n[{time.ctime()}] ⏰ Running scheduled job...")
    try:
        run_autoclose_overdue()
    except Exception as e:
        print(f"❌ Error in scheduled job: {e}")

def main():
    print("🚀 Scheduler started.")
    print("⏳ Job configured to run every 1 minute (for testing phase)...")
    
    schedule.every(1).minutes.do(job)

    # یک بار همان اول اجرا می‌کنیم تا مطمئن شویم کار می‌کند
    job()

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()