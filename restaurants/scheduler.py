from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
import os

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
        call_command,
        'cron',
        args=['playwright'],
        kwargs={'source': 'khu', 'campus': 'seoul'},
        id='playwright_khu_seoul',
        hour=6,
        minute=0,
        replace_existing=True
    )
    scheduler.add_job(
        call_command,
        'cron',
        args=['playwright'],
        kwargs={'source': 'khu', 'campus': 'global'},
        id='playwright_khu_global',
        hour=6,
        minute=0,
        replace_existing=True
    )
    
    # Run playwright scraping for HUFS every day at 6:00 AM
    scheduler.add_job(
        call_command,
        'cron',
        args=['playwright'],
        kwargs={'source': 'hufs', 'student': True},
        id='playwright_hufs_student',
        hour=6,
        minute=0,
        replace_existing=True
    )
    scheduler.add_job(
        call_command,
        'cron',
        args=['playwright'],
        kwargs={'source': 'hufs', 'student': False},
        id='playwright_hufs_staff',
        hour=6,
        minute=0,
        replace_existing=True
    )
    
    # Run playwright scraping for dorm every day at 6:00 AM
    scheduler.add_job(
        call_command,
        'cron',
        args=['playwright'],
        kwargs={'source': 'dorm'},
        id='playwright_dorm',
        hour=6,
        minute=0,
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
    
    scheduler.start()

def stop():
    """Stop the scheduler"""
    scheduler.shutdown()
