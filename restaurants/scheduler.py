from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
import threading

# Shared lock — ensures playwright jobs run one at a time even if cron fires them simultaneously
_playwright_lock = threading.Lock()

def _run_playwright(*args, **kwargs):
    """Acquire the lock before running playwright so jobs are queued, not concurrent."""
    with _playwright_lock:
        call_command(*args, **kwargs)

# Create scheduler 
# scheduler = BackgroundScheduler()
scheduler = BackgroundScheduler(timezone='Asia/Seoul')

def start():
    """Start the scheduler with scheduled jobs"""
    
    # Clear expired sessions daily at 3 AM
    # scheduler.add_job(
    #     call_command,
    #     'cron',
    #     args=['clearsessions'],
    #     id='clear_sessions',
    #     hour=3,
    #     minute=0,
    #     replace_existing=True
    # )
    
    # Run playwright scraping for KHU Seoul campus every Tuesday at 7:13 AM
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'khu', 'campus': 'seoul'},
        id='playwright_khu_seoul',
        day_of_week='tue',
        hour=7,
        minute=13,
        replace_existing=True
    )
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'khu', 'campus': 'global'},
        id='playwright_khu_global',
        day_of_week='tue',
        hour=7,
        minute=24,
        replace_existing=True
    )
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'hufs', 'student': True},
        id='playwright_hufs_student',
        day_of_week='tue',
        hour=7,
        minute=35,
        replace_existing=True
    )
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'hufs', 'student': False},
        id='playwright_hufs_staff',
        day_of_week='tue',
        hour=7,
        minute=46,
        replace_existing=True
    )
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'dorm'},
        id='playwright_dorm',
        day_of_week='tue',
        hour=7,
        minute=57,
        replace_existing=True
    )
    
    if not scheduler.running:
        scheduler.start()

def stop():
    """Stop the scheduler"""
    scheduler.shutdown()
