from __future__ import absolute_import

from datetime import timedelta

from celery.schedules import crontab

from reeach_will import settings
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reeach_will.settings')

app = Celery('reeach_will', include=['reeach_will.celery'],broker=settings.CELERY_BROKER_URL,backend=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings',namespace='celery')
app.autodiscover_tasks()



app.conf.beat_schedule ={
    'My_SmartList': {
        'task': 'client.tasks.SmartList',
        'schedule': crontab(minute=0,hour="*/12"),
    },
    'Coupon': {
        'task': 'client.tasks.CouponValidation',
        'schedule': crontab(minute=0,hour="*/12"),
    },
    'ScheduleBroadcast': {
        'task': 'client.tasks.ScheduleToSentBroadcast',
        'schedule': crontab(minute=0,hour="*/6"),
    },
    'DateBasedCampaign': {
        'task': 'client.tasks.CampaignStartForDateBasedTrigger',
        'schedule': crontab(minute=0,hour="*/6"),
    },
    'CompletedCampaign': {
        'task': 'client.tasks.RemoveComplateCampaign',
        'schedule': crontab(minute=0,hour="*/2"),
    },
    'SendReminderReferralCoupon': {
        'task': 'client.tasks.SendReferralCouponToContactUser',
        'schedule': crontab(minute=0,hour="*/12"),
    }
}