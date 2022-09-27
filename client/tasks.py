import json

import pytz
from client.models import ContactUser


from reeach_will.celery import app
from celery import shared_task
from celery.utils.log import get_task_logger
from .utils import SendingWindow
from .utils import CancelationTrigger

logger=get_task_logger(__name__)


@app.task
def sendnowsms(from_no,id,message,broad_id):
    from client.models import Client,ContactUser,BroadCast,Coupon,ContactUserCoupon,CustomFields, CustomFieldsValue, OneToOneMessage, ReferralCampaigns,ReferralCampaignToContact
    from twilio.rest import Client as twillio_client
    from datetime import datetime,timedelta
    from django.conf import settings

    logger.info('asdasdas')
    client=Client.objects.get(id=id)
    contact_no=ContactUser.objects.filter(client=client)
    broadcast=BroadCast.objects.get(id=broad_id)
    custom_fields=CustomFields.objects.filter(client_field=client)
    broadcast.contacts_count=contact_no.count()
    broadcast.save()
    coupon_obj=""
    coupon = Coupon.objects.filter(client_coupon=client,is_referral=False)
    for i in coupon:
        abc = "{{" + i.coupon_name + "}}"
        if abc in message:
            coupon_obj = i
    print(coupon_obj)

    # For Referral Campaign
    referral_camp_obj = ""
    referral_camps = ReferralCampaigns.objects.filter(client_rc=client)
    for rc in referral_camps:
        referral = "{{" + rc.ref_camp_name + "}}"
        if referral in message:
            referral_camp_obj = rc

    if client.account_sid:
        twi_client = twillio_client(client.account_sid, client.auth_token)
        for i in contact_no:
            if coupon_obj:
                user_coupon=ContactUserCoupon.objects.filter(user=i,user_coupon=coupon_obj).first()
                if not user_coupon:
                    user_coupon=ContactUserCoupon.objects.create(user=i,user_coupon=coupon_obj)
                    if coupon_obj.max_read_count:
                        coupon_obj.max_read_count += 1
                    else:
                        coupon_obj.max_read_count = 1
                    coupon_obj.save()
                abc="{{"+coupon_obj.coupon_name+"}}"
                message_check = message.replace("{{First Name}}", i.first_name or '')
                message_check = message_check.replace("{{Last Name}}", i.last_name or '')
                if i.birthday:
                    message_check = message_check.replace("{{Birthdate}}", datetime.strftime(i.birthday, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Birthdate}}", '')
                if i.anniversary:
                    message_check = message_check.replace("{{Anniversary}}",
                                                          datetime.strftime(i.anniversary, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Anniversary}}", '')
                message_check = message_check.replace(abc, f"{settings.COUPON_URL}{user_coupon.short_url}")
            else:
                message_check = message.replace("{{First Name}}", i.first_name or '')
                message_check = message_check.replace("{{Last Name}}", i.last_name or '')
                if i.birthday:
                    message_check = message_check.replace("{{Birthdate}}", datetime.strftime(i.birthday, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Birthdate}}", '')
                if i.anniversary:
                    message_check = message_check.replace("{{Anniversary}}",
                                                          datetime.strftime(i.anniversary, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Anniversary}}", '')

            if referral_camp_obj:
                referral_camp_user = ReferralCampaignToContact.objects.filter(contact_user=i, referral_camp=referral_camp_obj).first()
                if not referral_camp_user:
                    referral_camp_user = ReferralCampaignToContact.objects.create(contact_user=i, referral_camp=referral_camp_obj)
                    if referral_camp_obj.max_read_count:
                        referral_camp_obj.max_read_count += 1
                    else:
                        referral_camp_obj.max_read_count = 1
                    referral_camp_obj.save()
                referral_name = "{{" + referral_camp_obj.ref_camp_name + "}}"
                message_check = message_check.replace(referral_name, f"{settings.REFERRAL_CAMPAIGN_URL}{referral_camp_user.short_url}")
                
            for j in custom_fields:
                field_name = "{{"+j.field_name+"}}"
                custom_field_value = CustomFieldsValue.objects.filter(custom_field=j,contact_user=i).first()
                if custom_field_value:
                    if custom_field_value.custom_field.field_type == 'date':
                        new_date = datetime.strptime(custom_field_value.field_value, "%m-%d-%Y")
                        message_check = message_check.replace(field_name, datetime.strftime(new_date, "%d %B") or '')
                    else:
                        message_check = message_check.replace(field_name, custom_field_value.field_value or '')
                else:
                    message_check = message_check.replace(field_name, '')

            OneToOneMessage.objects.create(message=message,contact=i,client=client,is_send=True)
            message_obj = twi_client.messages.create(to=f'{i.phone_no}', from_=f'{from_no}', body=message_check)

@app.task
def sendnowlistsms(from_no,id,client_list,message,broad_id):
    from client.models import Client,ContactUser,BroadCast,ContactList,Coupon,ContactUserCoupon,CustomFields, CustomFieldsValue, OneToOneMessage, ReferralCampaigns,ReferralCampaignToContact
    from twilio.rest import Client as twillio_client
    from datetime import datetime
    from django.conf import settings
    logger.info('asdasdas')
    client=Client.objects.get(id=id)
    contact_obj = ContactUser.objects.none()
    client_list_obj = ContactList.objects.filter(id__in=client_list)
    for j in client_list_obj:
        contact_obj = contact_obj | j.contacts.all()
    contact_obj = contact_obj.distinct('id').order_by('id')
    custom_fields=CustomFields.objects.filter(client_field=client)
    broadcast=BroadCast.objects.get(id=broad_id)
    broadcast.contacts_count=contact_obj.count()
    broadcast.save()

    coupon_obj = ""
    coupon = Coupon.objects.filter(client_coupon=client,is_referral=False)
    for i in coupon:
        abc = "{{" + i.coupon_name + "}}"
        if abc in message:
            coupon_obj = i

    # For Referral Campaign
    referral_camp_obj = ""
    referral_camps = ReferralCampaigns.objects.filter(client_rc=client)
    for rc in referral_camps:
        referral = "{{" + rc.ref_camp_name + "}}"
        if referral in message:
            referral_camp_obj = rc

    if client.account_sid:
        twi_client = twillio_client(client.account_sid, client.auth_token)
        for i in contact_obj:
            if coupon_obj:
                user_coupon = ContactUserCoupon.objects.filter(user=i, user_coupon=coupon_obj).first()
                if not user_coupon:
                    user_coupon = ContactUserCoupon.objects.create(user=i, user_coupon=coupon_obj)
                    if coupon_obj.max_read_count:
                        coupon_obj.max_read_count += 1
                    else:
                        coupon_obj.max_read_count = 1
                    coupon_obj.save()
                abc = "{{" + coupon_obj.coupon_name + "}}"
                message_check = message.replace("{{First Name}}", i.first_name or '')
                message_check = message_check.replace("{{Last Name}}", i.last_name or '')
                if i.birthday:
                    message_check = message_check.replace("{{Birthdate}}", datetime.strftime(i.birthday, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Birthdate}}", '')
                if i.anniversary:
                    message_check = message_check.replace("{{Anniversary}}",
                                                          datetime.strftime(i.anniversary, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Anniversary}}", '')
                message_check = message_check.replace(abc, f"{settings.COUPON_URL}{user_coupon.short_url}")
            else:
                message_check = message.replace("{{First Name}}", i.first_name or '')
                message_check = message_check.replace("{{Last Name}}", i.last_name or '')
                if i.birthday:
                    message_check = message_check.replace("{{Birthdate}}", datetime.strftime(i.birthday, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Birthdate}}", '')
                if i.anniversary:
                    message_check = message_check.replace("{{Anniversary}}",
                                                          datetime.strftime(i.anniversary, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Anniversary}}", '')

            if referral_camp_obj:
                referral_camp_user = ReferralCampaignToContact.objects.filter(contact_user=i, referral_camp=referral_camp_obj).first()
                if not referral_camp_user:
                    referral_camp_user = ReferralCampaignToContact.objects.create(contact_user=i, referral_camp=referral_camp_obj)
                    if referral_camp_obj.max_read_count:
                        referral_camp_obj.max_read_count += 1
                    else:
                        referral_camp_obj.max_read_count = 1
                    referral_camp_obj.save()
                referral_name = "{{" + referral_camp_obj.ref_camp_name + "}}"
                message_check = message_check.replace(referral_name, f"{settings.REFERRAL_CAMPAIGN_URL}{referral_camp_user.short_url}")

            for j in custom_fields:
                field_name = "{{"+j.field_name+"}}"
                custom_field_value = CustomFieldsValue.objects.filter(custom_field=j,contact_user=i).first()
                if custom_field_value:
                    if custom_field_value.custom_field.field_type == 'date':
                        new_date = datetime.strptime(custom_field_value.field_value, "%m-%d-%Y")
                        message_check = message_check.replace(field_name, datetime.strftime(new_date, "%d %B") or '')
                    else:
                        message_check = message_check.replace(field_name, custom_field_value.field_value or '')
                else:
                    message_check = message_check.replace(field_name, '')

            OneToOneMessage.objects.create(message=message_check,contact=i,client=client,is_send=True)
            message_obj = twi_client.messages.create(to=f'{i.phone_no}', from_=f'{from_no}', body=message_check)

@app.task
def Schedulesms(id,message,broad_id,sch_date):
    from client.models import Client,ContactUser,BroadCast,Coupon,ContactUserCoupon,CustomFields, CustomFieldsValue, OneToOneMessage, ReferralCampaigns,ReferralCampaignToContact
    from twilio.rest import Client as twillio_client
    from datetime import datetime,timedelta
    from django.conf import settings

    logger.info('asdasdas')
    client=Client.objects.get(id=id)
    contact_no=ContactUser.objects.filter(client=client)
    custom_fields=CustomFields.objects.filter(client_field=client)
    broadcast=BroadCast.objects.get(id=broad_id)
    broadcast.contacts_count=contact_no.count()
    broadcast.save()
    coupon_obj = ""
    coupon = Coupon.objects.filter(client_coupon=client,is_referral=False)
    for i in coupon:
        abc = "{{" + i.coupon_name + "}}"
        if abc in message:
            coupon_obj = i


    # For Referral Campaign
    referral_camp_obj = ""
    referral_camps = ReferralCampaigns.objects.filter(client_rc=client)
    for rc in referral_camps:
        referral = "{{" + rc.ref_camp_name + "}}"
        if referral in message:
            referral_camp_obj = rc

    if client.account_sid:
        twi_client = twillio_client(client.account_sid, client.auth_token)
        for i in contact_no:
            if coupon_obj:
                user_coupon = ContactUserCoupon.objects.filter(user=i, user_coupon=coupon_obj).first()
                if not user_coupon:
                    user_coupon = ContactUserCoupon.objects.create(user=i, user_coupon=coupon_obj)

                    if coupon_obj.max_read_count:
                        coupon_obj.max_read_count += 1
                    else:
                        coupon_obj.max_read_count = 1
                    coupon_obj.save()
                abc = "{{" + coupon_obj.coupon_name + "}}"
                message_check = message.replace("{{First Name}}", i.first_name or '')
                message_check = message_check.replace("{{Last Name}}", i.last_name or '')
                if i.birthday:
                    message_check = message_check.replace("{{Birthdate}}", datetime.strftime(i.birthday, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Birthdate}}", '')
                if i.anniversary:
                    message_check = message_check.replace("{{Anniversary}}",
                                                          datetime.strftime(i.anniversary, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Anniversary}}", '')
                message_check = message_check.replace(abc, f"{settings.COUPON_URL}{user_coupon.short_url}")
            else:
                message_check = message.replace("{{First Name}}", i.first_name or '')
                message_check = message_check.replace("{{Last Name}}", i.last_name or '')
                if i.birthday:
                    message_check = message_check.replace("{{Birthdate}}", datetime.strftime(i.birthday, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Birthdate}}", '')
                if i.anniversary:
                    message_check = message_check.replace("{{Anniversary}}",
                                                          datetime.strftime(i.anniversary, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Anniversary}}", '')

            if referral_camp_obj:
                referral_camp_user = ReferralCampaignToContact.objects.filter(contact_user=i, referral_camp=referral_camp_obj).first()
                if not referral_camp_user:
                    referral_camp_user = ReferralCampaignToContact.objects.create(contact_user=i, referral_camp=referral_camp_obj)
                    if referral_camp_obj.max_read_count:
                        referral_camp_obj.max_read_count += 1
                    else:
                        referral_camp_obj.max_read_count = 1
                    referral_camp_obj.save()
                referral_name = "{{" + referral_camp_obj.ref_camp_name + "}}"
                message_check = message_check.replace(referral_name, f"{settings.REFERRAL_CAMPAIGN_URL}{referral_camp_user.short_url}")

            for j in custom_fields:
                field_name = "{{"+j.field_name+"}}"
                custom_field_value = CustomFieldsValue.objects.filter(custom_field=j,contact_user=i).first()
                if custom_field_value:
                    if custom_field_value.custom_field.field_type == 'date':
                        new_date = datetime.strptime(custom_field_value.field_value, "%m-%d-%Y")
                        message_check = message_check.replace(field_name, datetime.strftime(new_date, "%d %B") or '')
                    else:
                        message_check = message_check.replace(field_name, custom_field_value.field_value or '')
                else:
                    message_check = message_check.replace(field_name, '')

            # OneToOneMessage.objects.create(message=message,contact=i,client=client,is_send=True)
            message_obj = twi_client.messages.create(to=f'{i.phone_no}',
                            messaging_service_sid=client.message_service_id,
                            body=message_check,
                            schedule_type='fixed',
                            send_at=sch_date)



@app.task
def Schedulelistsms(id,client_list,message,broad_id,sch_date):
    from client.models import Client,ContactUser,BroadCast,ContactList,ContactUserCoupon,Coupon,CustomFields, CustomFieldsValue, OneToOneMessage, ReferralCampaigns,ReferralCampaignToContact
    from twilio.rest import Client as twillio_client
    from datetime import datetime
    from django.conf import settings
    logger.info('asdasdas')
    client=Client.objects.get(id=id)
    custom_fields=CustomFields.objects.filter(client_field=client)
    contact_obj = ContactUser.objects.none()
    client_list_obj = ContactList.objects.filter(id__in=client_list)
    for j in client_list_obj:
        contact_obj = contact_obj | j.contacts.all()
    contact_obj = contact_obj.distinct('id').order_by('id')
    broadcast=BroadCast.objects.get(id=broad_id)
    broadcast.contacts_count=contact_obj.count()
    broadcast.save()
    coupon_obj = ""
    coupon = Coupon.objects.filter(client_coupon=client,is_referral=False)
    for i in coupon:
        abc = "{{" + i.coupon_name + "}}"
        if abc in message:
            coupon_obj = i

    # For Referral Campaign
    referral_camp_obj = ""
    referral_camps = ReferralCampaigns.objects.filter(client_rc=client)
    for rc in referral_camps:
        referral = "{{" + rc.ref_camp_name + "}}"
        if referral in message:
            referral_camp_obj = rc

    if client.account_sid:
        twi_client = twillio_client(client.account_sid, client.auth_token)
        for i in contact_obj:
            if coupon_obj:
                user_coupon = ContactUserCoupon.objects.filter(user=i, user_coupon=coupon_obj).first()
                if not user_coupon:
                    user_coupon = ContactUserCoupon.objects.create(user=i, user_coupon=coupon_obj)
                    if coupon_obj.max_read_count:
                        coupon_obj.max_read_count += 1
                    else:
                        coupon_obj.max_read_count = 1
                    coupon_obj.save()
                abc = "{{" + coupon_obj.coupon_name + "}}"
                message_check = message.replace("{{First Name}}", i.first_name or '')
                message_check = message_check.replace("{{Last Name}}", i.last_name or '')
                if i.birthday:
                    message_check = message_check.replace("{{Birthdate}}", datetime.strftime(i.birthday, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Birthdate}}", '')
                if i.anniversary:
                    message_check = message_check.replace("{{Anniversary}}",
                                                          datetime.strftime(i.anniversary, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Anniversary}}", '')
                message_check = message_check.replace(abc, f"{settings.COUPON_URL}{user_coupon.short_url}")
            else:
                message_check = message.replace("{{First Name}}", i.first_name or '')
                message_check = message_check.replace("{{Last Name}}", i.last_name or '')
                if i.birthday:
                    message_check = message_check.replace("{{Birthdate}}", datetime.strftime(i.birthday, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Birthdate}}", '')
                if i.anniversary:
                    message_check = message_check.replace("{{Anniversary}}",
                                                          datetime.strftime(i.anniversary, "%d %B") or '')
                else:
                    message_check = message_check.replace("{{Anniversary}}", '')


            if referral_camp_obj:
                referral_camp_user = ReferralCampaignToContact.objects.filter(contact_user=i, referral_camp=referral_camp_obj).first()
                if not referral_camp_user:
                    referral_camp_user = ReferralCampaignToContact.objects.create(contact_user=i, referral_camp=referral_camp_obj)
                    if referral_camp_obj.max_read_count:
                        referral_camp_obj.max_read_count += 1
                    else:
                        referral_camp_obj.max_read_count = 1
                    referral_camp_obj.save()
                referral_name = "{{" + referral_camp_obj.ref_camp_name + "}}"
                message_check = message_check.replace(referral_name, f"{settings.REFERRAL_CAMPAIGN_URL}{referral_camp_user.short_url}")

            for j in custom_fields:
                field_name = "{{"+j.field_name+"}}"
                custom_field_value = CustomFieldsValue.objects.filter(custom_field=j,contact_user=i).first()
                if custom_field_value:
                    if custom_field_value.custom_field.field_type == 'date':
                        new_date = datetime.strptime(custom_field_value.field_value, "%m-%d-%Y")
                        message_check = message_check.replace(field_name, datetime.strftime(new_date, "%d %B") or '')
                    else:
                        message_check = message_check.replace(field_name, custom_field_value.field_value or '')
                else:
                    message_check = message_check.replace(field_name, '')
            
            # OneToOneMessage.objects.create(message=message,contact=i,client=client,is_send=True)
            message_obj = twi_client.messages.create(to=f'{i.phone_no}',
                                                     messaging_service_sid=client.message_service_id,
                                                     body=message_check,
                                                     schedule_type='fixed',
                                                     send_at=sch_date)



@shared_task
def SmartList():
    from client.models import ContactList,ContactUser
    contact_list=ContactList.objects.filter(is_smart=True)

    if contact_list:

        for i in contact_list:
            contact = ContactUser.objects.filter(client=i.list_owner)
            if i.rev_type:
                print('revenue')
                if i.rev_type == "3":
                    contact = contact.filter(sales__range=[i.rev_from, i.rev_to])
                elif i.rev_type == "1":
                    contact = contact.filter(sales__lt=i.rev_val)
                elif i.rev_type == "2":
                    contact = contact.filter(sales__gt=i.rev_val)

            if i.date_type:
                print('date val')
                if i.date_type == "3":
                    print('date3')
                    contact = contact.filter(created_at__date__range=[i.date_from, i.date_to])
                elif i.date_type == "2":
                    print('date2')
                    contact = contact.filter(created_at__date__lt=i.date_val)
                elif i.date_type == "1":
                    print('date1')
                    contact = contact.filter(created_at__date__gt=i.date_val)


            if contact:
                for j in contact:
                    i.contacts.add(j)

                i.save()

@shared_task
def CouponValidation():
    from client.models import Coupon
    from datetime import datetime,timedelta

    coupons=Coupon.objects.filter(is_no_end=False)
    today=datetime.now().date()
    print(today, 'today_date')
    if coupons:
        for i in coupons:
            print(i)
            print(i.is_valid)
            print(i.valid_to.date(),'coupon_date')

            if today > i.valid_to.date():
                i.is_valid=False
                i.save()

@shared_task
def ScheduleToSentBroadcast():
    from client.models import BroadCast,Client
    from datetime import datetime,timedelta
    import pytz
    broadcast=BroadCast.objects.filter(is_schdeule=True)
    today = datetime.utcnow()
    if broadcast:
        for i in broadcast:
            if today.strftime('%d/%m/%Y %I:%M%p') > i.sch_date.strftime('%d/%m/%Y %I:%M%p'):
                i.is_schdeule=False
                i.is_sent=True
                i.created_at=i.sch_date
                i.save()


@shared_task
def ClientSendEmailForActivation(agency_id,activity):
    from client.models import Client
    from admin_user.utils import send_templated_email
    from django.conf import settings
    client=Client.objects.filter(aegency__id=agency_id)
    if activity:
        print('yes')
        if client:
            for i in client:
                i.is_active = True
                i.save()
                # dyanmic_data_for_template = {
                #     'link': f'{settings.LOCAL_EMAIL}/client/client_login',
                #     'first_name': i.first_name,
                #     'last_name': i.last_name,
                #     'agency_name':i.aegency.business_name,
                #     'subject':settings.CLIENT_ACTIVE_SUBJECT
                # }
                # try:
                #     send_templated_email(i.email, settings.ACTIVE_USER_TEMPLATE, dyanmic_data_for_template)
                # except Exception as e:
                #     print(e)
                #     print(e.__traceback__)
                #     pass
    else:
        if client:
            print('no')
            for i in client:
                i.is_active = False
                i.save()
                # dyanmic_data_for_template = {
                #     'link': f'{settings.LOCAL_EMAIL}/client/client_login',
                #     'first_name': i.first_name,
                #     'last_name': i.last_name,
                #     'agency_name':i.aegency.business_name,
                #     'subject':settings.CLIENT_INACTIVE_SUBJECT
                # }
                # try:
                #     send_templated_email(i.email, settings.INACTIVE_USER_TEMPLATE, dyanmic_data_for_template)
                # except Exception as e:
                #     print(e)
                #     print(e.__traceback__)
                #     pass

@app.task
def DateBasedCampaginActivatToContact(contact_id,campaign_id):
    from client.models import ContactUser,CampaignAction,Campaign,Coupon,ContactUserCoupon,ContactToCampaign,ClientPhoneNumber,CustomFields, CustomFieldsValue,ReferralCampaigns,ReferralCampaignToContact
    from twilio.rest import Client as twillio_client
    from datetime import datetime,timedelta
    from django.conf import settings

    contact=ContactUser.objects.get(id=contact_id)
    custom_fields=CustomFields.objects.filter(client_field=contact.client)
    campaign=Campaign.objects.filter(id__in=campaign_id)
    print(campaign)
    schedule_time=datetime.utcnow()
    for i in campaign:
        if i not in contact.active_campaign.all():
            contact.active_campaign.add(i)
            contact.save()
            campaign_action=CampaignAction.objects.filter(campaign_action=i).order_by('order')
            print(campaign_action)
            if campaign_action:
                for j in campaign_action:
                    print(campaign_action.reverse()[0],'last--------------------------------------------')
                    print(j.action)
                    if j.action['action_type'] == "text_message":
                        coupon_obj=""
                        coupon = Coupon.objects.filter(client_coupon=i.client_campaign,is_referral=False)
                        for c in coupon:
                            abc = "{{" + c.coupon_name + "}}"
                            if abc in j.action['action_value']:
                                coupon_obj = c

                        # For Referral Campaign
                        referral_camp_obj = ""
                        referral_camps = ReferralCampaigns.objects.filter(client_rc=i.client_campaign)
                        for rc in referral_camps:
                            referral = "{{" + rc.ref_camp_name + "}}"
                            if referral in j.action['action_value']:
                                referral_camp_obj = rc

                        if coupon_obj:
                            user_coupon = ContactUserCoupon.objects.filter(user=contact, user_coupon=coupon_obj).first()
                            if not user_coupon:
                                user_coupon = ContactUserCoupon.objects.create(user=contact, user_coupon=coupon_obj)
                                if coupon_obj.max_read_count:
                                    coupon_obj.max_read_count += 1
                                else:
                                    coupon_obj.max_read_count = 1
                                coupon_obj.save()
                            abc = "{{" + coupon_obj.coupon_name + "}}"
                            message_check = j.action['action_value'].replace("{{First Name}}", contact.first_name or '')
                            message_check = message_check.replace("{{Last Name}}", contact.last_name or '')
                            if contact.birthday:
                                message_check = message_check.replace("{{Birthdate}}",
                                                                      datetime.strftime(contact.birthday, "%d %B") or '')
                            else:
                                message_check = message_check.replace("{{Birthdate}}", '')
                            if contact.anniversary:
                                message_check = message_check.replace("{{Anniversary}}",
                                                                      datetime.strftime(contact.anniversary,
                                                                                        "%d %B") or '')
                            else:
                                message_check = message_check.replace("{{Anniversary}}", '')
                            message_check = message_check.replace(abc,
                                                                  f"{settings.COUPON_URL}{user_coupon.short_url}")
                        else:
                            message_check = j.action['action_value'].replace("{{First Name}}", contact.first_name or '')
                            message_check = message_check.replace("{{Last Name}}", contact.last_name or '')
                            if contact.birthday:
                                message_check = message_check.replace("{{Birthdate}}",
                                                                      datetime.strftime(contact.birthday, "%d %B") or '')
                            else:
                                message_check = message_check.replace("{{Birthdate}}", '')
                            if contact.anniversary:
                                message_check = message_check.replace("{{Anniversary}}",
                                                                      datetime.strftime(contact.anniversary,
                                                                                        "%d %B") or '')
                            else:
                                message_check = message_check.replace("{{Anniversary}}", '')

                        if referral_camp_obj:
                            referral_camp_user = ReferralCampaignToContact.objects.filter(contact_user=contact, referral_camp=referral_camp_obj).first()
                            if not referral_camp_user:
                                referral_camp_user = ReferralCampaignToContact.objects.create(contact_user=contact, referral_camp=referral_camp_obj)
                                if referral_camp_obj.max_read_count:
                                    referral_camp_obj.max_read_count += 1
                                else:
                                    referral_camp_obj.max_read_count = 1
                                referral_camp_obj.save()
                            referral_name = "{{" + referral_camp_obj.ref_camp_name + "}}"
                            message_check = message_check.replace(referral_name, f"{settings.REFERRAL_CAMPAIGN_URL}{referral_camp_user.short_url}")

                        for cf in custom_fields:
                            field_name = "{{"+cf.field_name+"}}"
                            custom_field_value = CustomFieldsValue.objects.filter(custom_field=cf,contact_user=contact).first()
                            if custom_field_value:
                                if custom_field_value.custom_field.field_type == 'date':
                                    new_date = datetime.strptime(custom_field_value.field_value, "%m-%d-%Y")
                                    message_check = message_check.replace(field_name, datetime.strftime(new_date, "%d %B") or '')
                                else:
                                    message_check = message_check.replace(field_name, custom_field_value.field_value or '')
                            else:
                                message_check = message_check.replace(field_name, '')

                        try:
                            print(i.send_phone.phone_number)
                            print(contact.phone_no,'contact')
                            obj=CampaignActionForTextMessage.apply_async(args=[message_check,i.client_campaign.id,
                                                                               f'{contact.phone_no}',f'{i.send_phone.phone_number}'],eta=schedule_time)
                            CtoC_obj=ContactToCampaign.objects.create(campaign_action=j,contact_user=contact,date_time=schedule_time)
                            temp_dict={
                                'type':'text',
                                'message':message_check,
                                'schedule_task': obj.id,
                            }
                            CtoC_obj.type=temp_dict
                            if j.order == campaign_action.reverse()[0].order:
                                CtoC_obj.is_last=True
                            CtoC_obj.save()
                        except Exception as e:
                            print(e)
                            print(e.__traceback__.tb_lineno)

                    elif j.action['action_type'] == "time_delay":
                        if j.action['action_value']['time'] == "minute":
                            schedule_time=schedule_time+timedelta(minutes=int(j.action['action_value']['time_val']))
                        elif j.action['action_value']['time'] == "hours":
                            schedule_time = schedule_time+ timedelta(hours=int(j.action['action_value']['time_val']))
                        elif j.action['action_value']['time'] == "day":
                            schedule_time = schedule_time+ timedelta(days=int(j.action['action_value']['time_val']))
                        CtoC_obj=ContactToCampaign.objects.create(campaign_action=j,contact_user=contact,date_time=schedule_time)
                        if j.order == campaign_action.reverse()[0].order:
                            CtoC_obj.is_last=True
                        CtoC_obj.save()

                    elif j.action['action_type'] == "wait_until":
                        if j.action['action_value']['time_am'] == "AM":
                            hour=int(j.action['action_value']['hour'])
                            min=int(j.action['action_value']['minute'])
                            print(hour,'hour')
                            print(min,'minute')
                            # select_date_time=datetime.today()
                            # select_date_time=select_date_time.replace(hour=hour,minute=min)
                            if i.client_campaign.time_zone:
                                local = pytz.timezone(f'{i.client_campaign.time_zone.value}')
                                select_date_time=datetime.now(local)
                                now = select_date_time
                                if hour == 12:
                                    hour = 0
                                select_date_time=select_date_time.replace(hour=hour,minute=min)
                                if select_date_time < now:
                                    select_date_time = select_date_time + timedelta(days=1)
                                utc_dt = select_date_time.astimezone(pytz.utc)
                            else:
                                utc_dt=datetime.utcnow()
                                now = utc_dt
                                utc_dt=utc_dt.replace(hour=hour,minute=min)
                                if utc_dt < now:
                                    utc_dt = utc_dt + timedelta(days=1)

                        else:
                            if int(j.action['action_value']['hour']) == 12:
                                hour = int(j.action['action_value']['hour'])
                            else:
                                hour = int(j.action['action_value']['hour'])+12
                            min = int(j.action['action_value']['minute'])
                            print(hour, 'hour')
                            print(min, 'minute')
                            # select_date_time = datetime.today()
                            # select_date_time = select_date_time.replace(hour=hour, minute=min)
                            if i.client_campaign.time_zone:
                                local = pytz.timezone(f'{i.client_campaign.time_zone.value}')
                                select_date_time=datetime.now(local)
                                now = select_date_time
                                select_date_time=select_date_time.replace(hour=hour,minute=min)
                                if select_date_time < now:
                                    select_date_time = select_date_time + timedelta(days=1)
                                utc_dt = select_date_time.astimezone(pytz.utc)
                            else:
                                utc_dt=datetime.utcnow()
                                now = utc_dt
                                utc_dt=utc_dt.replace(hour=hour,minute=min)
                                if utc_dt < now:
                                    utc_dt = utc_dt + timedelta(days=1)


                        # if i.client_campaign.time_zone:
                        #     print(select_date_time.tzinfo,'asdasdasda508')
                        #     local = pytz.timezone(f'{i.client_campaign.time_zone}')
                        #     local_dt = local.localize(select_date_time, is_dst=None)
                        #     utc_dt = local_dt.astimezone(pytz.utc)
                        # else:
                        #     local = pytz.timezone('Australia/Sydney')
                        #     local_dt = local.localize(select_date_time, is_dst=None)
                        #     utc_dt = local_dt.astimezone(pytz.utc)
                        schedule_time = utc_dt
                        CtoC_obj=ContactToCampaign.objects.create(campaign_action=j,contact_user=contact,date_time=schedule_time)
                        if j.order == campaign_action.reverse()[0].order:
                            CtoC_obj.is_last=True
                        CtoC_obj.save()
                        # if utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ") < schedule_time.strftime("%Y-%m-%dT%H:%M:%SZ"):
                        #     print(schedule_time,'schedule_time............................1')
                        # else:
                        #     schedule_time=utc_dt+timedelta(days=1)
                        #     print(schedule_time,'schedule_time............................2')

                    elif j.action['action_type'] == "tag_action":
                        try:
                            print([k['id'] for k in j.action['action_value']])
                            tag_id=[k['id'] for k in j.action['action_value']]
                            print(type(tag_id),'533')
                            obj= CampaignActionForTag.apply_async(args=[tag_id,contact_id,i.client_campaign.id],eta=schedule_time)
                            print(obj.__dict__,'asdasdas')
                            CtoC_obj = ContactToCampaign.objects.create(campaign_action=j, contact_user=contact,
                                                                        date_time=schedule_time)
                            temp_dict = {
                                'type': 'tag',
                                'tag_value':j.action['action_value'],
                                'schedule_task':obj.id,
                            }
                            
                            CtoC_obj.type = temp_dict
                            if j.order == campaign_action.reverse()[0].order:
                                CtoC_obj.is_last=True
                            CtoC_obj.save()
                        except Exception as e:
                            print(e)
                            print(e.__traceback__.tb_lineno)


@app.task
def CampaignActionForTag(tags_id,contact,client):
    from client.models import Campaign, Tags

    print(tags_id,'tags_id')

    tags = Tags.objects.filter(id__in=tags_id,client_tag__id=client)
    print(tags,'...................................................tags')
    cont = ContactUser.objects.get(id=contact)
    cont.tags.add(*tags)

    campaign=Campaign.objects.filter(trigger_type__trigger_type="tag",client_campaign__id=client)
    campaign_id=[]
    for i in campaign:
        for j in i.trigger_type['trigger_value']:
            if j['id'] in tags_id:
                campaign_id.append(i.id)
    print(campaign_id)
    CampaginActivatToContact.delay(contact,campaign_id)

@app.task
def CampaignActionForTextMessage(message,client_id,to_contact,from_contact):
    from client.models import Client, ContactUser, OneToOneMessage
    from twilio.rest import Client as twillio_client
    from datetime import datetime, timedelta
    from django.conf import settings
    client=Client.objects.get(id=client_id)
    print(to_contact,'to_contact')
    contact=ContactUser.objects.filter(client=client,phone_no=to_contact).first()
    OneToOneMessage.objects.create(message=message,contact=contact,client=client,is_send=True)
    try:
        if client.account_sid:
            twi_client = twillio_client(client.account_sid, client.auth_token)
            message_obj = twi_client.messages.create(to=f'{to_contact}',
                                                 from_=f'{from_contact}',
                                                 body=message)
    except Exception as e:
        print(e)
        print(e.__traceback__.tb_lineno)


@shared_task
def CampaignStartForDateBasedTrigger():
    from client.models import Campaign,ContactUser,CustomFields,CustomFieldsValue
    from datetime import datetime,timedelta

    campaign=Campaign.objects.filter(trigger_type__trigger_type="date")
    for i in campaign:
        print(i.name)
        custom_field = CustomFields.objects.filter(field_type__in=('date','datetime-local'),client_field=i.client_campaign)
        if i.client_campaign.time_zone:
            local = pytz.timezone(f'{i.client_campaign.time_zone.value}')
            today=datetime.now(local).date()
        else:
            today=datetime.utcnow().date()
        if i.trigger_type['trigger_value']['date_based'][0].lower() == "birthday":
            contacts=ContactUser.objects.filter(client=i.client_campaign,birthday__month=today.month,birthday__day=(today+timedelta(days=int(i.trigger_type['trigger_value']['before_days']))).day)
            for j in contacts:
                DateBasedCampaginActivatToContact.delay(j.id, [i.id])
        elif i.trigger_type['trigger_value']['date_based'][0].lower() == "anniversary":
            contacts=ContactUser.objects.filter(client=i.client_campaign,anniversary__month=today.month,anniversary__day=(today+timedelta(days=int(i.trigger_type['trigger_value']['before_days']))).day)
            for j in contacts:
                DateBasedCampaginActivatToContact.delay(j.id, [i.id])
        else:
            for c in custom_field:
                if i.trigger_type['trigger_value']['date_based'][0] == c.field_name:
                    custom_field_value = CustomFieldsValue.objects.filter(custom_field=c)
                    for cfv in custom_field_value:
                        if c.field_type == 'datetime-local':
                            new_date = datetime.strptime(cfv.field_value, "%m-%d-%Y %H:%M %p")
                        else:
                            new_date = datetime.strptime(cfv.field_value, "%m-%d-%Y")
                        if new_date.date() == today+timedelta(days=int(i.trigger_type['trigger_value']['before_days'])):
                            DateBasedCampaginActivatToContact.delay(cfv.contact_user.id, [i.id])




@app.task
def CancelCampaignReply(contact,campaig_id):
    pass

@app.task
def CampaginActivatToContact(contact_id,campaign_id):
    from client.models import ContactUser,CampaignAction,Campaign,Coupon,ContactUserCoupon,ContactToCampaign,ClientPhoneNumber,CustomFields, CustomFieldsValue,ReferralCampaigns,ReferralCampaignToContact
    from twilio.rest import Client as twillio_client
    from datetime import datetime,timedelta
    from django.conf import settings

    contact=ContactUser.objects.get(id=contact_id)
    custom_fields=CustomFields.objects.filter(client_field=contact.client)
    campaign=Campaign.objects.filter(id__in=campaign_id)
    print(campaign)
    schedule_time=datetime.utcnow()
    for i in campaign:
        if i in contact.active_campaign.all() and i.is_limit:
            schedule_time=SendingWindow(i.id,schedule_time)
            limit_multiple_message=i.limit_message
            obj=CampaignActionForTextMessage.apply_async(args=[limit_multiple_message,i.client_campaign.id,f'{contact.phone_no}',f'{i.send_phone.phone_number}'],eta=schedule_time)
        else:
            contact.active_campaign.add(i)
            contact.save()
            CancelationTrigger( [i.id],contact_id)
            campaign_action=CampaignAction.objects.filter(campaign_action=i).order_by('order')
            # print(campaign_action)
            if campaign_action:
                for j in campaign_action:
                    print(campaign_action.reverse()[0],'last--------------------------------------------')
                    print(j.action)
                    if j.action['action_type'] == "text_message":
                        coupon_obj=""
                        coupon = Coupon.objects.filter(client_coupon=i.client_campaign,is_referral=False)
                        for c in coupon:
                            abc = "{{" + c.coupon_name + "}}"
                            if abc in j.action['action_value']:
                                coupon_obj = c

                        # For Referral Campaign
                        referral_camp_obj = ""
                        referral_camps = ReferralCampaigns.objects.filter(client_rc=i.client_campaign)
                        for rc in referral_camps:
                            referral = "{{" + rc.ref_camp_name + "}}"
                            if referral in j.action['action_value']:
                                referral_camp_obj = rc

                        if coupon_obj:
                            user_coupon = ContactUserCoupon.objects.filter(user=contact, user_coupon=coupon_obj).first()
                            if not user_coupon:
                                user_coupon = ContactUserCoupon.objects.create(user=contact, user_coupon=coupon_obj)
                                if coupon_obj.max_read_count:
                                    coupon_obj.max_read_count += 1
                                else:
                                    coupon_obj.max_read_count = 1
                                coupon_obj.save()
                            abc = "{{" + coupon_obj.coupon_name + "}}"
                            message_check = j.action['action_value'].replace("{{First Name}}", contact.first_name or '')
                            message_check = message_check.replace("{{Last Name}}", contact.last_name or '')
                            if contact.birthday:
                                message_check = message_check.replace("{{Birthdate}}",
                                                                    datetime.strftime(contact.birthday, "%d %B") or '')
                            else:
                                message_check = message_check.replace("{{Birthdate}}", '')
                            if contact.anniversary:
                                message_check = message_check.replace("{{Anniversary}}",
                                                                    datetime.strftime(contact.anniversary,
                                                                                        "%d %B") or '')
                            else:
                                message_check = message_check.replace("{{Anniversary}}", '')
                            message_check = message_check.replace(abc,
                                                                f"{settings.COUPON_URL}{user_coupon.short_url}")
                        else:
                            message_check = j.action['action_value'].replace("{{First Name}}", contact.first_name or '')
                            message_check = message_check.replace("{{Last Name}}", contact.last_name or '')
                            if contact.birthday:
                                message_check = message_check.replace("{{Birthdate}}",
                                                                    datetime.strftime(contact.birthday, "%d %B") or '')
                            else:
                                message_check = message_check.replace("{{Birthdate}}", '')
                            if contact.anniversary:
                                message_check = message_check.replace("{{Anniversary}}",
                                                                    datetime.strftime(contact.anniversary,
                                                                                        "%d %B") or '')
                            else:
                                message_check = message_check.replace("{{Anniversary}}", '')

                        if referral_camp_obj:
                            referral_camp_user = ReferralCampaignToContact.objects.filter(contact_user=contact, referral_camp=referral_camp_obj).first()
                            if not referral_camp_user:
                                referral_camp_user = ReferralCampaignToContact.objects.create(contact_user=contact, referral_camp=referral_camp_obj)
                                if referral_camp_obj.max_read_count:
                                    referral_camp_obj.max_read_count += 1
                                else:
                                    referral_camp_obj.max_read_count = 1
                                referral_camp_obj.save()
                            referral_name = "{{" + referral_camp_obj.ref_camp_name + "}}"
                            message_check = message_check.replace(referral_name, f"{settings.REFERRAL_CAMPAIGN_URL}{referral_camp_user.short_url}")
                        
                        for cf in custom_fields:
                            field_name = "{{"+cf.field_name+"}}"
                            custom_field_value = CustomFieldsValue.objects.filter(custom_field=cf,contact_user=contact).first()
                            if custom_field_value:
                                if custom_field_value.custom_field.field_type == 'date':
                                    new_date = datetime.strptime(custom_field_value.field_value, "%m-%d-%Y")
                                    message_check = message_check.replace(field_name, datetime.strftime(new_date, "%d %B") or '')
                                else:
                                    message_check = message_check.replace(field_name, custom_field_value.field_value or '')
                            else:
                                message_check = message_check.replace(field_name, '')

                        try:
                            print(i.send_phone.phone_number)
                            print(contact.phone_no,'contact')
                            print(schedule_time,'dasgdfasghfdghasfdghasfdghasfdghasfghf')
                            schedule_time=SendingWindow(i.id,schedule_time)
                            obj=CampaignActionForTextMessage.apply_async(args=[message_check,i.client_campaign.id,
                                                                            f'{contact.phone_no}',f'{i.send_phone.phone_number}'],eta=schedule_time)
                            CtoC_obj=ContactToCampaign.objects.create(campaign_action=j,contact_user=contact,date_time=schedule_time)
                            temp_dict={
                                'type':'text',
                                'message':message_check,
                                'schedule_task': obj.id,
                            }
                            CtoC_obj.type=temp_dict
                            if j.order == campaign_action.reverse()[0].order:
                                CtoC_obj.is_last=True
                            CtoC_obj.save()
                        except Exception as e:
                            print(e)
                            print(e.__traceback__.tb_lineno)

                    elif j.action['action_type'] == "time_delay":
                        if j.action['action_value']['time'] == "minute":
                            schedule_time=schedule_time+timedelta(minutes=int(j.action['action_value']['time_val']))
                        elif j.action['action_value']['time'] == "hours":
                            schedule_time = schedule_time+ timedelta(hours=int(j.action['action_value']['time_val']))
                        elif j.action['action_value']['time'] == "day":
                            schedule_time = schedule_time+ timedelta(days=int(j.action['action_value']['time_val']))
                        CtoC_obj=ContactToCampaign.objects.create(campaign_action=j,contact_user=contact,date_time=schedule_time)
                        if j.order == campaign_action.reverse()[0].order:
                            CtoC_obj.is_last=True
                        CtoC_obj.save()

                    elif j.action['action_type'] == "wait_until":
                        if j.action['action_value']['time_am'] == "AM":
                            hour=int(j.action['action_value']['hour'])
                            min=int(j.action['action_value']['minute'])
                            print(hour,'hour')
                            print(min,'minute')
                            # select_date_time=datetime.today()
                            # select_date_time=select_date_time.replace(hour=hour,minute=min)
                            if i.client_campaign.time_zone:
                                local = pytz.timezone(f'{i.client_campaign.time_zone.value}')
                                select_date_time=datetime.now(local)
                                now = select_date_time
                                if hour == 12:
                                    hour = 0
                                select_date_time=select_date_time.replace(hour=hour,minute=min)
                                if select_date_time < now:
                                    select_date_time = select_date_time + timedelta(days=1)
                                utc_dt = select_date_time.astimezone(pytz.utc)
                            else:
                                utc_dt=datetime.utcnow()
                                now = utc_dt
                                utc_dt=utc_dt.replace(hour=hour,minute=min)
                                if utc_dt < now:
                                    utc_dt = utc_dt + timedelta(days=1)

                        else:
                            if int(j.action['action_value']['hour']) == 12:
                                hour = int(j.action['action_value']['hour'])
                            else:
                                hour = int(j.action['action_value']['hour'])+12
                            min = int(j.action['action_value']['minute'])
                            print(hour, 'hour')
                            print(min, 'minute')
                            # select_date_time = datetime.today()
                            # select_date_time = select_date_time.replace(hour=hour, minute=min)
                            if i.client_campaign.time_zone:
                                local = pytz.timezone(f'{i.client_campaign.time_zone.value}')
                                select_date_time=datetime.now(local)
                                now = select_date_time
                                print(now,'.......................................now')
                                select_date_time=select_date_time.replace(hour=hour,minute=min)
                                print(select_date_time,'....................................select_date_time')
                                if select_date_time < now:
                                    select_date_time = select_date_time + timedelta(days=1)
                                utc_dt = select_date_time.astimezone(pytz.utc)
                            else:
                                utc_dt=datetime.utcnow()
                                now = utc_dt
                                utc_dt=utc_dt.replace(hour=hour,minute=min)
                                if utc_dt < now:
                                    utc_dt = utc_dt + timedelta(days=1)

                        # print(local,'....................................Client Timezone')
                        # print(select_date_time,'....................................LOacl Time')
                        # print(utc_dt,'....................................UTC Time')

                        # if i.client_campaign.time_zone:
                        #     print(select_date_time.tzinfo,'asdasdasda508')
                        #     local = pytz.timezone(f'{i.client_campaign.time_zone}')
                        #     local_dt = local.localize(select_date_time, is_dst=None)
                        #     utc_dt = local_dt.astimezone(pytz.utc)
                        # else:
                        #     local = pytz.timezone('Australia/Sydney')
                        #     local_dt = local.localize(select_date_time, is_dst=None)
                        #     utc_dt = local_dt.astimezone(pytz.utc)
                        schedule_time = utc_dt
                        CtoC_obj=ContactToCampaign.objects.create(campaign_action=j,contact_user=contact,date_time=schedule_time)
                        if j.order == campaign_action.reverse()[0].order:
                            CtoC_obj.is_last=True
                        CtoC_obj.save()
                        # if utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ") < schedule_time.strftime("%Y-%m-%dT%H:%M:%SZ"):
                        #     print(schedule_time,'schedule_time............................1')
                        # else:
                        #     schedule_time=utc_dt+timedelta(days=1)
                        # utc_dt = schedule_time.astimezone(local)

                    elif j.action['action_type'] == "tag_action":
                        try:
                            print([k['id'] for k in j.action['action_value']])
                            tag_id=[k['id'] for k in j.action['action_value']]
                            print(type(tag_id),'533')
                            schedule_time=SendingWindow(i.id,schedule_time)
                            obj= CampaignActionForTag.apply_async(args=[tag_id,contact_id,i.client_campaign.id],eta=schedule_time)
                            print(obj.__dict__,'asdasdas')
                            CtoC_obj = ContactToCampaign.objects.create(campaign_action=j, contact_user=contact,
                                                                        date_time=schedule_time)
                            temp_dict = {
                                'type': 'tag',
                                'tag_value':j.action['action_value'],
                                'schedule_task':obj.id,
                            }
                            
                            CtoC_obj.type = temp_dict
                            if j.order == campaign_action.reverse()[0].order:
                                CtoC_obj.is_last=True
                            CtoC_obj.save()
                        except Exception as e:
                            print(e)
                            print(e.__traceback__.tb_lineno)


@app.task
def CancelCampaignToContact(contact_id,new_active_campaign_list):
    from client.models import ContactUser

    contact = ContactUser.objects.get(id=contact_id)
    old_active_campaign_list = []


@shared_task
def RemoveComplateCampaign():
    from client.models import ContactToCampaign, ContactUser, Campaign
    from datetime import datetime

    current_time=datetime.utcnow()
    complate_compaign = ContactToCampaign.objects.filter(is_last=True, date_time__lt=current_time)
    for i in complate_compaign:
        contact = i.contact_user
        campaign = i.campaign_action.campaign_action

        contact_user = ContactUser.objects.get(id=contact.id)
        contact_user.active_campaign.remove(campaign)
        contact_user.save()
        
        cam_obj = Campaign.objects.filter(id=i.campaign_action.campaign_action.id).first()
        cam_obj.complate_count=int(cam_obj.complate_count)+1
        cam_obj.save()

        camp = ContactToCampaign.objects.filter(campaign_action__campaign_action=campaign,contact_user=contact)
        for c in camp:
            if c.type:
                app.control.revoke(c.type["schedule_task"])
            c.delete()


@shared_task
def SendReferralCouponToContactUser():
    from client.models import ContactUserCoupon,ReferralCampaignToContact,Coupon,OneToOneMessage, Client, ClientPhoneNumber
    from twilio.rest import Client as twillio_client
    from django.conf import settings
    from datetime import datetime,timedelta
    from .templatetags.tag_filter import digit_roundoff

    users_coupon = ContactUserCoupon.objects.all()

    for i in users_coupon:
        if i.is_read == False:
            coupon = i.user_coupon
            contact = i.user
            
            client = Client.objects.filter(id=contact.client.id).first()
            client_phone_no = ClientPhoneNumber.objects.filter(client_phone=client,is_default=True).first()

            coupon_obj = Coupon.objects.filter(id=coupon.id).first()
            if coupon_obj.is_referral == True:
                contact_referral = ReferralCampaignToContact.objects.filter(referral_camp__ref_coupon=coupon_obj,refered_user=contact).first()
                if contact_referral:

                    if coupon_obj.discount_type == "percentage":
                        dis_value = digit_roundoff(coupon_obj.discount_value)
                        dis_value = f'{dis_value}%'
                    else:
                        dis_value = digit_roundoff(coupon_obj.discount_value)
                        dis_value = f'${dis_value}'

                    if client.time_zone:
                        local = pytz.timezone(f'{client.time_zone.value}')
                        # today=today.replace(tzinfo=pytz.UTC)
                        # local_dt = today.astimezone(local)
                        today = datetime.now(local)
                        local_dt = today #.replace(hour=8,minute=0)
                        utc_dt = local_dt.astimezone(pytz.utc)
                    else:
                        today=datetime.utcnow()
                        utc_dt=today #.replace(hour=8,minute=0)

                    if i.second_message_sent == False:
                        user_coup_obj = ContactUserCoupon.objects.filter(user_coupon=coupon_obj,user=contact,created_at__month=today.month,created_at__day=(today-timedelta(days=6)).day)
                        if user_coup_obj:
                            message = f'{client.business_name}: Just a quick reminder your {dis_value} OFF voucher expires next week. Click here to redeem in-store: {settings.COUPON_URL}{i.short_url}'
                            
                            try:
                                obj=CampaignActionForTextMessage.apply_async(args=[message,client.id,
                                                                            f'{contact.phone_no}',f'{client_phone_no.phone_number}'],eta=utc_dt)
                            except Exception as e:
                                print(e)
                                print(e.__traceback__.tb_lineno)
                            i.second_message_sent = True
                            i.save()
                    else:
                        user_coup_obj = ContactUserCoupon.objects.filter(user_coupon=coupon_obj,user=contact,created_at__month=today.month,created_at__day=(today-timedelta(days=13)).day)
                        if user_coup_obj:
                            message = f'{client.business_name}: Hurry! Your {dis_value} OFF voucher expires in 2 days. Come on in and see us now. Click here to redeem in-store: {settings.COUPON_URL}{i.short_url}'
                            
                            try:
                                obj=CampaignActionForTextMessage.apply_async(args=[message,client.id,
                                                                            f'{contact.phone_no}',f'{client_phone_no.phone_number}'],eta=utc_dt)
                            except Exception as e:
                                print(e)
                                print(e.__traceback__.tb_lineno)
        
