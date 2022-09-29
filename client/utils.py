import random
import string

from django.http import JsonResponse
import pytz

from datetime import datetime, tzinfo
import time

from client.models import Campaign, ContactToCampaign
from reeach_will.celery import app
import json


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def SendingWindow(campaign_id,schedule_time):
    from client.models import Campaign
    from datetime import datetime,timedelta
    import calendar
    
    campaign = Campaign.objects.filter(id=campaign_id).first()
    
    if campaign.is_sending == True:
        if campaign.client_campaign.time_zone:
            # print(schedule_time,'=========================================')
            local = pytz.timezone(f'{campaign.client_campaign.time_zone.value}')
            # print(local,"............................local timezo")
            # local_dt = local.localize(schedule_time, is_dst=None)
            schedule_time=schedule_time.replace(tzinfo=pytz.UTC)
            local_dt = schedule_time.astimezone(local)
            print(local_dt,"...............................1local")
        else:
            local = pytz.timezone('Australia/Sydney')
            # local_dt = local.localize(schedule_time, is_dst=None)
            schedule_time=schedule_time.replace(tzinfo=pytz.UTC)
            local_dt = schedule_time.astimezone(local)
            print(local_dt,"...............................2")

        schedule_day = calendar.day_name[local_dt.weekday()][:3]
        campaign_schedule_day = [i.name.lower() for i in campaign.sending_days.all()]
    
        i = 0
        while i >= 0:
            if schedule_day.lower() in campaign_schedule_day:
                print(campaign.start_time.strftime("%H:%M:%S"),"campaginstart time")
                if local_dt.strftime("%H:%M:%S") >= campaign.start_time.strftime("%H:%M:%S") and local_dt.strftime("%H:%M:%S") <= campaign.end_time.strftime("%H:%M:%S"):
                    print(local_dt,"...............................3")
                    utc_dt = local_dt.astimezone(pytz.utc)
                    print(utc_dt,"...............................4")
                    return utc_dt
                else:
                    if local_dt.strftime("%H:%M:%S") < campaign.start_time.strftime("%H:%M:%S"):
                        new_local_dt=local_dt
                    else:
                        new_local_dt = local_dt + timedelta(days=1)
            else:
                new_local_dt = local_dt + timedelta(days=1)
            local_dt = new_local_dt.replace(hour=campaign.start_time.hour, minute=campaign.start_time.minute)
            schedule_day = calendar.day_name[local_dt.weekday()][:3] 
            i = i + 1

    else:
        return schedule_time


def CancelationTrigger(campaign_id, contact_id):
    
    campaigns = ContactToCampaign.objects.filter(campaign_action__campaign_action__id__in=campaign_id, contact_user__id=contact_id)
    if campaigns:
        for campaign in campaigns:
            if campaign.type:
                app.control.revoke(campaign.type["schedule_task"])
            campaign.delete()
    return JsonResponse({"status":True})