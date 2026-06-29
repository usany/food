from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
import os
import threading

# Shared lock — ensures playwright jobs run one at a time even if cron fires them simultaneously
_playwright_lock = threading.Lock()

def _run_playwright(*args, **kwargs):
    """Acquire the lock before running playwright so jobs are queued, not concurrent."""
    with _playwright_lock:
        call_command(*args, **kwargs)

# Create scheduler
scheduler = BackgroundScheduler()

def start():
    """Start the scheduler with scheduled jobs"""
    
    # Clear expired sessions daily at 3 AM
    scheduler.add_job(
        call_command,
        'cron',
        args=['clearsessions'],
        id='clear_sessions',
        hour=3,
        minute=0,
        replace_existing=True
    )
    
    # Run playwright scraping for KHU Seoul campus every day at 6:00 AM
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'khu', 'campus': 'seoul'},
        id='playwright_khu_seoul',
        hour=15,
        minute=57,
        replace_existing=True
    )
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'khu', 'campus': 'global'},
        id='playwright_khu_global',
        hour=15,
        minute=45,
        replace_existing=True
    )
    
    # Run playwright scraping for HUFS every day at 6:00 AM
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'hufs', 'student': True},
        id='playwright_hufs_student',
        hour=15,
        minute=45,
        replace_existing=True
    )
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'hufs', 'student': False},
        id='playwright_hufs_staff',
        hour=15,
        minute=45,
        replace_existing=True
    )
    
    # Run playwright scraping for dorm every day at 6:00 AM
    scheduler.add_job(
        _run_playwright,
        'cron',
        args=['playwright'],
        kwargs={'source': 'dorm'},
        id='playwright_dorm',
        hour=15,
        minute=45,
        replace_existing=True
    )
    
    # Add more jobs here as needed
    # Example: Run custom command every hour
    # scheduler.add_job(
    #     call_command,
    #     'cron',
    #     args=['your_hourly_task'],
    #     id='hourly_task',
    #     hour='*',
    #     minute=0,
    #     replace_existing=True
    # )
    
    # Example: Run backup daily at 2 AM
    # scheduler.add_job(
    #     call_command,
    #     'cron',
    #     args=['backup'],
    #     id='daily_backup',
    #     hour=2,
    #     minute=0,
    #     replace_existing=True
    # )
    
    if not scheduler.running:
        scheduler.start()

def stop():
    """Stop the scheduler"""
    scheduler.shutdown()
