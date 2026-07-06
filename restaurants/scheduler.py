from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
import threading
# import os

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
    scheduler.add_job(
        call_command,
        'cron',
        args=['clearsessions'],
        id='clear_sessions',
        hour=16,
        minute=16,
        replace_existing=True
    )
    
    # Run playwright scraping for KHU Seoul campus every day at 6:00 AM
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'khu', 'campus': 'seoul'},
        id='playwright_khu_seoul',
        hour=21,
        minute=50,
        replace_existing=True
    )
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'khu', 'campus': 'global'},
        id='playwright_khu_global',
        hour=21,
        minute=50,
        replace_existing=True
    )
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'hufs', 'student': True},
        id='playwright_hufs_student',
        hour=21,
        minute=50,
        replace_existing=True
    )
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'hufs', 'student': False},
        id='playwright_hufs_staff',
        hour=21,
        minute=50,
        replace_existing=True
    )
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'dorm'},
        id='playwright_dorm',
        hour=16,
        minute=16,
        replace_existing=True
    )
    
    if not scheduler.running:
        scheduler.start()

def stop():
    """Stop the scheduler"""
    scheduler.shutdown()
