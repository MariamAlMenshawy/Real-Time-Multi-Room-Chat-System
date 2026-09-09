from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_system.settings')

app = Celery('tasks',broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/'),include=['chat_messages.tasks'])

app.conf.beat_schedule = {
    'daily-activity-digest' : {
        'task' : 'chat_messages.tasks.send_daily_activity_digest',
        'schedule' : 86400,  # 24 hours
    }
}

app.conf.timezone = 'EET'