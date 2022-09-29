from cgi import print_arguments
from http import client
from multiprocessing import context
import random
import re
import string
from django import views

import pytz
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from admin_user.models import Address, Admin
from admin_user.utils import send_templated_email
from .models import Client, ContactUser, Tags, TimeZone, ContactList, ClientPhoneNumber, BroadCast, Coupon, \
    ContactUserCoupon, Keyword, Days, Campaign, CampaignAction, ContactToCampaign, CustomFields, CustomFieldsValue, \
    DoubleOptinCampaign,OneToOneMessage,ReferralCampaigns, ReferralCampaignToContact,ReferralRewardCouponContactUser
from aegency_user.models import AgencyUser
from .forms import ClientChangeForm,ClientEditProfileForm,ContactCreateForm,ContactChangeForm
from aegency_user.forms import AddressChangeForm
# Create your views here.
from django.views import View
from .serializer import ContactUserSerializer, ContactListSerializer, ContactUserCouponSerializer, TagsSerializer, CustomFielsValueSerializer,ContactUserReferralCampaignSerializer,ReferralRewardCouponContactUserSerializer
from client_user.models import ClientUser
from twilio.rest import Client as twillio_client
import json
from .tasks import sendnowsms, sendnowlistsms, Schedulesms, Schedulelistsms, ScheduleToSentBroadcast, SmartList, \
    CouponValidation, CampaginActivatToContact, CampaignStartForDateBasedTrigger, CancelCampaignReply, \
    CampaignActionForTextMessage, RemoveComplateCampaign, SendReferralCouponToContactUser
from datetime import date, datetime,timedelta
from django.db.models import Count, Sum, F
from django.db.models.functions import Coalesce
from .utils import CancelationTrigger

from .templatetags.tag_filter import digit_roundoff


class ClientPermissionRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        print(request,"request")
        print(args,"args")
        print(kwargs['id'],"kwargs")
        print(request.user.id)
        if not request.user.is_authenticated:
            return redirect('client-login')
        try:
            client = Client.objects.get(id=kwargs['id'])
            agency = AgencyUser.objects.filter(id=request.user.id).first()
            print(agency)
            if agency:
                if agency.id != client.aegency.id:
                    return render(request, "error_page.html")
            elif client.id != request.user.id:
                return render(request, "error_page.html")
        except:
            return render(request, "error_page.html")
        return super().dispatch(request, *args, **kwargs)


class ClientLoginView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'client_login.html')
        if request.user:
            client=Client.objects.filter(id=request.user.id).first()
            if not client:
                logout(request)
                return render(request, 'client_login.html')
        return redirect('client-dashboard',id=request.user.id)

    def post(self, request):
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember=request.POST.get('remember')
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if not email and not password:
            messages.error(request,'Please enter E-mail and Password')
            return redirect(request.path)
        if not email:
            messages.error(request,'Please enter E-mail')
            return redirect(request.path)
        if not password:
            messages.error(request,'Please enter Password')
            return redirect(request.path)

        if not re.fullmatch(regex, email):
            messages.error(request, 'Invalid Email.')
            return redirect(request.path)

        user = Client.objects.filter(email=email).first()
        if user:
            if not user.is_active:
                messages.error(request,'Your account is currently inactive. Please contact your Administrator')
                return redirect(request.path)
            account = authenticate(email=email, password=password)

            if account:
                login(request, account)
                if not remember:
                    request.session.set_expiry(0)
                return redirect('client-dashboard',id=account.id)
            else:
                messages.error(request, 'Please enter proper E-mail and Password')
                return redirect(request.path)
        else:
            messages.error(request, 'User does not exists')
            return redirect(request.path)

class ClientLogoutView(View):
    def get(self, request):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        if agency:
            logout(request)
            return redirect('agency-login')
        else:
            logout(request)
            return redirect('client-login')

class ClientForgetPasswordView(View):
    def get(self,request):
        return render(request,'client_forget.html')

    def post(self,request):
        email=request.POST['email']
        if not email:
            messages.error(request,"Please enter Email")
            return redirect(request.path)
        user = Client.objects.filter(email=email).first()
        print(user)
        if user:
            domain = (f'http://{user.aegency.whitelabeldomian}' if user.aegency.host.is_verified else settings.LOCAL_EMAIL) if user.aegency.host else settings.LOCAL_EMAIL
            user.is_forget=True
            user.save()
            dyanmic_data_for_template={
                'link':f'{domain}/client/client-reset-password/{user.unique_id}',
                'first_name':user.first_name,
                'last_name':user.last_name,
                'agency_name' : user.aegency.business_name,
                'subject':settings.CLIENT_FORGOT_PASSWORD

            }
            print(user.email,'............................user.email')
            print(settings.FORGOT_TEMPLATE,'............................settings.FORGOT_TEMPLATE')
            print(dyanmic_data_for_template,'............................sdyanmic_data_for_template')
            try:
                send_templated_email(user.email, settings.FORGOT_TEMPLATE, dyanmic_data_for_template)
                messages.success(request, 'E-mail sent successfully')
            except:
                messages.error(request, 'E-mail has not been sent')
            return render(request,'client_forget.html')
        else:
            messages.error(request,'User does not exists')
            return render(request,'client_forget.html')

class ClientSetPasswordView(View):
    def get(self,request,uuid):
        user=Client.objects.filter(unique_id=uuid).first()
        if user.is_forget:
            return render(request,'client_setpassword.html',{'uuid':uuid})
        else:
            messages.error(request,"Link has been expired")
            return render(request,'client_invalid.html')

    def post(self,request,uuid):
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if not password and not confirm_password:
            messages.error(request,"Please enter Password and Confirm Password")
            return redirect(request.path)

        user = Client.objects.filter(unique_id=uuid).first()
        if user:
            user.set_password(password)
            user.is_forget=False
            user.save()
            return redirect('client-login')
        return render(request,'client_invalid.html')

class ClientDashboardView(ClientPermissionRequiredMixin,View):
    def get(self,request,id):
        agency=AgencyUser.objects.filter(id=request.user.id).first()
        client=Client.objects.get(id=id)
        client_contact = ContactUser.objects.filter(client=client)
        total_sales = ContactUserCoupon.objects.filter(user__client=client).aggregate(Sum('amount'))
        coupon_list = list(Coupon.objects.filter(is_referral=False).values_list('id'))
        coupon_list = [i[0] for i in coupon_list]
        coupon_claimed = ContactUserCoupon.objects.filter(user__client=client,user_coupon__id__in=coupon_list,is_read=True).count()
        message_sent = BroadCast.objects.filter(client_brodcast=client,is_sent=True).count()
        context = {
            'client':client,
            'agency':agency,
            'client_contact':client_contact.order_by('-created_at')[:10],
            'count_contact':client_contact.count(),
            'total_sales':total_sales,
            'coupon_claimed':coupon_claimed,
            'message_sent':message_sent,
            }
        return render(request,'client_dashboard.html',context)
    
class ClientDashboardFilterView(View):
    def get(self,request):
        id = request.GET.get('id','')
        details = request.GET.get('details','')
        agency=AgencyUser.objects.filter(id=request.user.id).first()
        client=Client.objects.get(id=id)
        if details == 'Today':
            today = datetime.utcnow()
            client_contact = ContactUser.objects.filter(client=client,created_at__date=today.date())
            total_sales = ContactUserCoupon.objects.filter(user__client=client,updated_at__date=today.date()).aggregate(Sum('amount'))
            coupon_list = list(Coupon.objects.filter(is_referral=False).values_list('id'))
            coupon_list = [i[0] for i in coupon_list]
            coupon_claimed = ContactUserCoupon.objects.filter(user__client=client,user_coupon__id__in=coupon_list,is_read=True,updated_at__date=today.date()).count()
            message_sent = BroadCast.objects.filter(client_brodcast=client,is_sent=True,created_at__date=today.date()).count()

        if details == 'Last 7 Days':
            today = datetime.utcnow()
            startdate = datetime.utcnow() - timedelta(days=7)
            client_contact = ContactUser.objects.filter(client=client,created_at__range=[startdate,today])
            total_sales = ContactUserCoupon.objects.filter(user__client=client,updated_at__range=[startdate,today]).aggregate(Sum('amount'))
            coupon_list = list(Coupon.objects.filter(is_referral=False).values_list('id'))
            coupon_list = [i[0] for i in coupon_list]
            coupon_claimed = ContactUserCoupon.objects.filter(user__client=client,user_coupon__id__in=coupon_list,is_read=True,updated_at__range=[startdate,today]).count()
            message_sent = BroadCast.objects.filter(client_brodcast=client,is_sent=True,created_at__range=[startdate,today]).count()

        if details == 'This Month':
            today = datetime.utcnow()
            startdate = datetime.utcnow() - timedelta(days=today.day)
            client_contact = ContactUser.objects.filter(client=client,created_at__range=[startdate,today])
            total_sales = ContactUserCoupon.objects.filter(user__client=client,updated_at__range=[startdate,today]).aggregate(Sum('amount'))
            coupon_list = list(Coupon.objects.filter(is_referral=False).values_list('id'))
            coupon_list = [i[0] for i in coupon_list]
            coupon_claimed = ContactUserCoupon.objects.filter(user__client=client,user_coupon__id__in=coupon_list,is_read=True,updated_at__range=[startdate,today]).count()
            message_sent = BroadCast.objects.filter(client_brodcast=client,is_sent=True,created_at__range=[startdate,today]).count()

        if details == 'All':
            client_contact = ContactUser.objects.filter(client=client)
            total_sales = ContactUserCoupon.objects.filter(user__client=client).aggregate(Sum('amount'))
            coupon_list = list(Coupon.objects.filter(is_referral=False).values_list('id'))
            coupon_list = [i[0] for i in coupon_list]
            coupon_claimed = ContactUserCoupon.objects.filter(user__client=client,user_coupon__id__in=coupon_list,is_read=True).count()
            message_sent = BroadCast.objects.filter(client_brodcast=client,is_sent=True).count()
        print(client_contact,"********************************")
        context = {
            'client':client,
            'agency':agency,
            'client_contact':client_contact.order_by('-created_at')[:10],
            'count_contact':client_contact.count(),
            'total_sales':total_sales,
            'coupon_claimed':coupon_claimed,
            'message_sent':message_sent,
            }
        return render(request,'dashboard_details.html',context)


class ClientCampaignCreationView(ClientPermissionRequiredMixin,View):
    def get(self, request, id):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        return render(request, 'campaign_creation.html', {'client': client, 'agency': agency})


class ClientCampaignSettingView(ClientPermissionRequiredMixin,View):
    def get(self, request, id):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        client_form=ClientChangeForm(instance=client)
        address=AddressChangeForm(instance=client.address)
        context={
            'client': client,
            'agency': agency,
            'client_form':client_form,
            'add_form':address
        }
        return render(request, 'campaign_settings.html',context)

    def post(self,request,id):
        print('aaaaaaa')
        print(request.POST)
        aegency = AgencyUser.objects.filter(id=request.user.id).first()
        client=Client.objects.get(id=id)
        client_form = ClientChangeForm(request.POST,request.FILES,instance=client)
        address = AddressChangeForm(request.POST,request.FILES,instance=client.address)
        print(address.instance)
        context= {'add_form': address, 'client_form': client_form,'client':client,'agency':aegency}
        
        if client_form.is_valid():
            client_form.save()
            if address.is_valid():
                address.save()
                client_form.instance.address=address.instance
                client_form.save()
                messages.success(request,'Profile updated successfully')
            return redirect(request.path)
        
        return render(request, 'campaign_settings.html', context)

class ClientCampaignsView(ClientPermissionRequiredMixin,View):
    def get(self, request, id):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        campaign = Campaign.objects.filter(client_campaign=client).annotate(steps_cam=Count('campaignaction', distinct=True)).annotate(in_progress_cam=Count('contactuser', distinct=True))
        return render(request, 'campaigns.html', {'client': client, 'agency': agency,'campaign':campaign})

class ClientContactView(ClientPermissionRequiredMixin,View):
    def get(self, request, id):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        contact_form = ContactCreateForm()
        edit_form = ContactChangeForm()
        contact=ContactUser.objects.filter(client=client)
        tag=Tags.objects.filter(client_tag=client)
        campaign=Campaign.objects.filter(client_campaign=client).order_by('-created_at')
        contact_list=ContactList.objects.filter(list_owner=client)
        custom_fields = CustomFields.objects.filter(client_field=client)
        context={
            'client': client,
            'tag':tag ,
            'agency': agency,
            'forms':contact_form,
            'edit_form':edit_form,
            'contact':contact,
            'campaign':campaign,
            'list' :contact_list,
            'custom_fields' :custom_fields,
        }
        return render(request, 'client_contact.html', context)

    def post(self,request,id):
        print(request.POST)
        client = Client.objects.get(id=id)
        f_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_1 = request.POST.get('phone_1', '')
        phone_2 = request.POST.get('phone_2', '')
        tags = request.POST.getlist('tags[]', '')
        time_zone = request.POST.get('time_zone', '')
        birthday = request.POST.get('birthday', '')
        anniversary = request.POST.get('anniversary', '')
        phone_no=f"{phone_2}{phone_1}"
        custom_fields = request.POST.get('custom_fields','')
        custom_fields = json.loads(custom_fields)
        country_code_name = request.POST.get('country_code_name','')
        print(custom_fields)
        print(type(custom_fields))
        print(tags)
        print(birthday)
        print(anniversary)
        contact=ContactUser.objects.filter(client=client,phone_no=phone_no)

        if contact:
            response={
                'status':False,
                'message':"this contact already in system"
            }
            return JsonResponse(response)

        contact=ContactUser.objects.create(phone_no=phone_no,first_name=f_name,last_name=last_name,client=client)

        if country_code_name:
            contact.country_code_name=country_code_name

        if birthday:
            contact.birthday=birthday

        if anniversary:
            contact.anniversary=anniversary

        if tags:
            tag=Tags.objects.filter(id__in=tags)
            print(tag)
            if tag:
                for i in tag:
                    contact.tags.add(i)
            tags_id=[tags.id for tags in tag]
            campaign = Campaign.objects.filter(trigger_type__trigger_type="tag", client_campaign=client)
            print(campaign)
            campaign_id=[]
            for j in campaign:
                for k in j.trigger_type['trigger_value']:
                    print(k['id'])
                    if k['id'] in tags_id:
                        campaign_id.append(j.id)
            print(campaign_id)
            CampaginActivatToContact.delay(contact.id, campaign_id)


        if time_zone:
            time_zone_obj=TimeZone.objects.filter(id=time_zone).first()
            contact.time_zone=time_zone_obj

        if custom_fields:
            for i in custom_fields:
                
                custom_field_obj = CustomFields.objects.get(id=i['id'])
                custom_field_value = CustomFieldsValue.objects.create(custom_field=custom_field_obj,contact_user=contact,field_value=i['value'])

        contact.save()
        response={
            'status':True,
            'message':"contact user added successfully"
        }
        messages.success(request,'Contact User created successfully')
        return JsonResponse(response)


class ClientScheduleBroadcastView(ClientPermissionRequiredMixin,View):
    def get(self, request, id):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        contact_count=ContactUser.objects.filter(client=client).count()
        client_list=ContactList.objects.filter(list_owner=client)
        coupon=Coupon.objects.filter(client_coupon=client,is_valid=True,is_referral=False)
        custom_fields=CustomFields.objects.filter(client_field=client)
        referral_camp = ReferralCampaigns.objects.filter(client_rc=client)
        phone_no = ClientPhoneNumber.objects.filter(client_phone=client, is_default=True).first()
        if not phone_no:
            messages.error(request, 'Please purchase the number for Broadcast')
        context={
            'client': client,
            'agency': agency,
            'contact_count':contact_count,
            'client_list':client_list,
            'coupon':coupon,
            'hours':range(1,13),
            'minute':range(60),
            'custom_fields': custom_fields,
            'referral_camp': referral_camp,
        }
        return render(request, 'client_scheduled_broadcast.html', context)

    def post(self,request,id):
        print(request.POST)
        client = Client.objects.get(id=id)
        client_list=request.POST.getlist('list[]','')
        recipents=request.POST.get('recipents','')
        schdule=request.POST.get('schdule','')
        message=request.POST.get('message','')
        sch_date=request.POST.get('sch_date','')

        phone_no = ClientPhoneNumber.objects.filter(client_phone=client, is_default=True).first()
        if not phone_no:
            messages.error(request, 'Please purchase the number for Broadcast')
            return JsonResponse({'status':True})
        if schdule == "1":
            if recipents=="1":
                brodcast=BroadCast.objects.create(message=message,is_sent=True,client_brodcast=client)
                sendnowsms.delay(f'{phone_no.phone_number}',id,message, f'{brodcast.id}')
            else:
                if client_list:
                    brodcast = BroadCast.objects.create(message=message, is_sent=True, client_brodcast=client)
                    sendnowlistsms.delay(f'{phone_no.phone_number}', id, client_list,message, f'{brodcast.id}')
        elif schdule == "2":
            if recipents=="1":
                print(sch_date)
                date=datetime.strptime(sch_date,'%d/%m/%Y %I:%M%p')
                print(date)
                from_date = datetime.utcnow() + timedelta(hours=1, minutes=1)
                from_date = from_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                to_date = datetime.utcnow() + timedelta(days=7,hours=1)
                to_date = to_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                print(from_date)
                print(to_date)
                if client.time_zone:
                    local=pytz.timezone(client.time_zone.value)
                    local_dt = local.localize(date, is_dst=None)
                    utc_dt = local_dt.astimezone(pytz.utc)
                    utc_dt = utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                    print(utc_dt)
                else:
                    local = pytz.timezone('Australia/Sydney')
                    local_dt = local.localize(date, is_dst=None)
                    utc_dt = local_dt.astimezone(pytz.utc)
                    utc_dt=utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                    print(utc_dt)
                if utc_dt < from_date or utc_dt > to_date:
                    context = {
                        'status': False,
                        'msg': 'Please schedule broadcast after 1 hour and before 7 days',
                    }
                    print('asdasdasdsaas')
                    return JsonResponse(context)
                twi_client = twillio_client(client.account_sid, client.auth_token)
                if not client.message_service_id:
                    try:
                        message_service=twi_client.messaging.services.create(friendly_name=client.business_name)
                        client.message_service_id=message_service.sid
                        client.save()

                    except:
                        pass
                try:
                    phone_number=twi_client.messaging.services(client.message_service_id).phone_numbers.create(
                        phone_number_sid=phone_no.phone_sid
                    )
                except:
                    pass
                brodcast = BroadCast.objects.create(message=message, is_schdeule=True, client_brodcast=client,sch_date=utc_dt)
                Schedulesms.delay(id,message,f'{brodcast.id}',utc_dt)

            else:
                if client_list:
                    print(sch_date)
                    date = datetime.strptime(sch_date, '%d/%m/%Y %I:%M%p')
                    print(date,'date')
                    from_date = datetime.utcnow() + timedelta(hours=1, minutes=1)
                    from_date = from_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                    to_date = datetime.utcnow() + timedelta(days=7, hours=1)
                    to_date = to_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                    print(from_date)
                    print(to_date)
                    if client.time_zone:
                        local = pytz.timezone(client.time_zone.value)
                        local_dt = local.localize(date, is_dst=None)
                        utc_dt = local_dt.astimezone(pytz.utc)
                        utc_dt = utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                        print(utc_dt)
                    else:
                        local = pytz.timezone('Australia/Sydney')
                        local_dt = local.localize(date, is_dst=None)
                        utc_dt = local_dt.astimezone(pytz.utc)
                        utc_dt = utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                        print(utc_dt)
                    if utc_dt < from_date or utc_dt > to_date:
                        context = {
                            'status': False,
                            'msg': 'Please broadcast schedule after 1 hour or before 7 days',
                        }
                        print('asdasdasdsaas')
                        return JsonResponse(context)
                    twi_client = twillio_client(client.account_sid, client.auth_token)
                    if not client.message_service_id:
                        try:
                            message_service = twi_client.messaging.services.create(friendly_name=client.business_name,inbound_request_url=f'{settings.PHONE_WEBHOOK}')
                            client.message_service_id = message_service.sid
                            client.save()

                        except:
                            pass
                    try:
                        phone_number = twi_client.messaging.services(client.message_service_id).phone_numbers.create(
                            phone_number_sid=phone_no.phone_sid
                        )
                    except:
                        pass
                    brodcast = BroadCast.objects.create(message=message, is_schdeule=True, client_brodcast=client,
                                                        sch_date=utc_dt)
                    Schedulelistsms.delay(id,client_list, message, f'{brodcast.id}', utc_dt)

        context={
                'status':True,
                'msg':'done',
            }
        messages.success(request,'Broadcast sent successfully')
        return JsonResponse(context)


class ClientScheduleListBroadcastView(ClientPermissionRequiredMixin,View):
    def get(self, request, id):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        # contact_count=ContactUser.objects.filter(client=client).count()
        # client_list=ContactList.objects.filter(list_owner=client)
        broadcast=BroadCast.objects.filter(client_brodcast=client,is_schdeule=True)
        context={
            'client': client,
            'agency': agency,
            'broadcast':broadcast,
        }
        return render(request, 'broadcast_schedule.html', context)

class ClientSentListBroadcastView(ClientPermissionRequiredMixin,View):
    def get(self, request, id):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        # contact_count=ContactUser.objects.filter(client=client).count()
        # client_list=ContactList.objects.filter(list_owner=client)
        broadcast=BroadCast.objects.filter(client_brodcast=client,is_sent=True)
        context={
            'client': client,
            'agency': agency,
            'broadcast':broadcast,
        }
        return render(request, 'broadcast_sent.html', context)

def get_unique_coupon_code(coupon_code,client):
    code_check = Coupon.objects.filter(coupon_code=coupon_code,client_coupon=client)
    if code_check:
        a=''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        username = f"{a}"
        return get_unique_coupon_code(coupon_code,client)
    return coupon_code

class ClientCouponView(ClientPermissionRequiredMixin,View):
    def get(self, request, id):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        coupon=Coupon.objects.filter(client_coupon=client,is_referral=False)
        return render(request, 'coupon.html', {'client': client, 'agency': agency,'coupon':coupon})

    def post(self,request,id):
        client = Client.objects.get(id=id)
        name=request.POST.get('name','')
        dis_type=request.POST.get('dis_type','')
        dis_value=request.POST.get('dis_value','')
        spend=request.POST.get('spend','')
        valid_from=request.POST.get('valid_from','')
        valid_to=request.POST.get('valid_to','')
        is_end=request.POST.get('is_end','')
        valid_from=datetime.strptime(valid_from,"%d/%m/%Y")
        coupon_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        coupon_code_check=get_unique_coupon_code(coupon_code,client)
        print(type(is_end))
        print(is_end)

        if dis_type == "1":
            if not is_end=='false':
                coupon=Coupon.objects.create(coupon_name=name,discount_type='percentage',discount_value=dis_value,
                                         minmum_spend=spend,valid_from=valid_from,is_no_end=True,
                                             coupon_code=coupon_code_check,client_coupon=client)
            else:
                valid_to = datetime.strptime(valid_to, "%d/%m/%Y")
                coupon = Coupon.objects.create(coupon_name=name, discount_type='percentage', discount_value=dis_value,
                                               minmum_spend=spend, valid_from=valid_from, valid_to=valid_to,
                                               coupon_code=coupon_code_check,client_coupon=client)
        elif dis_type == "2":
            if not is_end=='false':
                coupon=Coupon.objects.create(coupon_name=name,discount_type='rs',discount_value=dis_value,
                                         minmum_spend=spend,valid_from=valid_from,is_no_end=True,
                                             coupon_code=coupon_code_check,client_coupon=client)
            else:
                valid_to = datetime.strptime(valid_to, "%d/%m/%Y")
                coupon = Coupon.objects.create(coupon_name=name, discount_type='rs', discount_value=dis_value,
                                               minmum_spend=spend, valid_from=valid_from, valid_to=valid_to,
                                               coupon_code=coupon_code_check,client_coupon=client)

        context={
            'status':True,
        }
        messages.success(request,'Coupon created successfully')
        return JsonResponse(context)


class CouponDeleteView(View):

    def get(self, request,id):
        print(id)
        coupon = Coupon.objects.get(id=id)
        client=coupon.client_coupon
        if coupon:
            coupon.delete()
            messages.success(request,'Coupon deleted successfully')
            return redirect('client-coupon',id=client.id)
        return render(request, 'coupon.html')

class GetListNameUnique(View):

    def get(self,request,id):
        client=Client.objects.get(id=id)
        name=request.GET.get('list_name','')
        client_list=ContactList.objects.filter(list_owner=client,name=name)
        if client_list:
            context={
                'status':False,
                'msg':'List Name already exists'
            }
            return JsonResponse(context)
        return JsonResponse({'status':True,'msg':'done'})

class ClientListView(ClientPermissionRequiredMixin,View):
    def get(self, request, id):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        contact=ContactUser.objects.filter(client=client)
        contact_list=ContactList.objects.filter(list_owner=client)
        return render(request, 'client_list.html', {'client': client, 'agency': agency,'contact':contact,'list':contact_list})

    def post(self,request,id):
        contact_id=request.POST.getlist('contact_id[]','')
        revenue_select=request.POST.get('revenue_select','')
        rev_from=request.POST.get('rev_from','')
        rev_to=request.POST.get('rev_to','')
        revenue_val=request.POST.get('revenue_val','')
        date_select=request.POST.get('date_select','')
        date_val=request.POST.get('date_val','')
        date_from=request.POST.get('date_from','')
        date_to=request.POST.get('date_to','')
        name=request.POST.get('list_name','')
        client=Client.objects.get(id=id)


        if contact_id:
            contact=ContactUser.objects.filter(id__in=contact_id)
            if not contact:
                context={
                    'status':False,
                    'msg':'List does not contain any contact'
                }
                return JsonResponse(context)
            contact_list = ContactList.objects.create(name=name, list_owner=client,is_static=True)
            for i in contact:
                contact_list.contacts.add(i)
            contact_list.is_static=True

        if revenue_select in ["1","2","3"] or date_select in ["1","2","3"]:
            print('all val')
            contact=ContactUser.objects.filter(client=client)
            if revenue_select:
                print('revenue')
                if revenue_select == "3":
                    contact=contact.filter(sales__range=[rev_from,rev_to])
                elif revenue_select == "1":
                    contact = contact.filter(sales__lt=revenue_val)
                elif revenue_select == "2":
                    contact = contact.filter(sales__gt=revenue_val)

            if date_select:
                print('date val')
                if date_select == "3":
                    print('date3')
                    contact=contact.filter(created_at__date__range=[date_from,date_to])
                elif date_select == "2":
                    print('date2')
                    contact = contact.filter(created_at__date__lt=date_val)
                elif date_select == "1":
                    print('date1')
                    contact = contact.filter(created_at__date__gt=date_val)
            # if not contact:
            #     context = {
            #         'status': False,
            #         'msg': 'List does not contain any contact'
            #     }
            #     return JsonResponse(context)
            contact_list = ContactList.objects.create(name=name, list_owner=client,is_smart=True)

            if revenue_select:
                contact_list.rev_type = revenue_select
                if revenue_select == "3":
                    contact_list.rev_from=rev_from
                    contact_list.rev_to=rev_to
                elif revenue_select == "1":
                    contact_list.rev_val=revenue_val
                elif revenue_select == "2":
                    contact_list.rev_val = revenue_val

            if date_select:
                contact_list.date_type=date_select
                if date_select == "3":
                    contact_list.date_from=date_from
                    contact_list.date_to = date_to
                elif date_select == "2":
                    contact_list.date_val = date_val
                elif date_select == "1":
                    contact_list.date_val = date_val

            contact_list.save()
            for i in contact:
                contact_list.contacts.add(i)
            contact_list.is_static = True
            contact_list.save()
        response={
            'status':True,
            'message':"List created successfully"
        }
        messages.success(request,'List created successfully')
        return JsonResponse(response)



class ClientAccountSettingView(LoginRequiredMixin,View):
    login_url = 'client-login'

    def get(self,request):
        client=Client.objects.get(id=request.user.id)
        form = ClientEditProfileForm(instance=client)
        return render(request,'client_account_setting.html', {'form': form,'client':client})

    def post(self, request):
        client = Client.objects.get(id=request.user.id)
        form = ClientEditProfileForm(request.POST, request.FILES, instance=client)
        context = {"form": form,'client':client}
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(request.path)
        return render(request, 'client_account_setting.html', context=context)

class EditContactView(View):
    def get(self,request):
        contact_id=request.GET.get('contact_id','')
        contact=ContactUser.objects.get(id=contact_id)
        ser=ContactUserSerializer(contact)
        campaign = ContactToCampaign.objects.filter(contact_user=contact_id)
        custom_fields_value = CustomFieldsValue.objects.filter(contact_user=contact)
        custom_ser=CustomFielsValueSerializer(custom_fields_value, many=True)
        print(campaign)
        print(type(ser.data))
        print(type(contact.phone_no))
        print(contact.phone_no.country_code)
        print(contact.phone_no.national_number)

        # res = model_to_dict(contact)

        response = {
            'status': True,
            'message': 'user created successfull',
            'contact': ser.data,
            'custom_field_value':custom_ser.data,
        }

        return JsonResponse(response)

    def post(self,request):
        print(request.POST)
        contact_id = request.POST.get('contact_id', '')

        f_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_1 = request.POST.get('phone_1', '')
        phone_2 = request.POST.get('phone_2', '')
        tags = request.POST.getlist('tags[]', '')
        active_campaigns = request.POST.getlist('active_campaigns[]', '')
        time_zone = request.POST.get('time_zone', '')
        birthday = request.POST.get('birthday', '')
        anniversary = request.POST.get('anniversary', '')
        country_code_name = request.POST.get('country_code_name', '')
        phone_no = f"{phone_1}{phone_2}"

        custom_fields = request.POST.get('custom_fields','')
        custom_fields = json.loads(custom_fields)

        contact = ContactUser.objects.get(id=contact_id)
        old_tags = contact.tags.all()
        old_tags = [i.id for i in old_tags]
        print(old_tags,'................................old')
        contact.tags.clear()

        client = Client.objects.filter(id=contact.client.id).first()

        if active_campaigns:
            new_active_campaigns=[int(i) for i in active_campaigns]
            remove_campaign=[]

            for j in contact.active_campaign.all():
                if j.id not in new_active_campaigns:
                    remove_campaign.append(j.id)
            CancelationTrigger(remove_campaign,contact.id)

            campaign = Campaign.objects.filter(id__in=new_active_campaigns)
            contact.active_campaign.clear()
            if campaign:
                for i in campaign:
                    contact.active_campaign.add(i)
        else:
            remove_campaign=[i.id for i in contact.active_campaign.all()]
            CancelationTrigger(remove_campaign,contact_id)

            contact.active_campaign.clear()
              

        if phone_no:
            contact.phone_no=phone_no
        if f_name:
            contact.first_name=f_name
        if last_name:
            contact.last_name=last_name
        if birthday:
            contact.birthday = birthday
        if anniversary:
            contact.anniversary = anniversary

        if country_code_name:
            contact.country_code_name=country_code_name

        if tags:
            tag = Tags.objects.filter(id__in=tags)
            print(tag)
            if tag:
                for i in tag:
                    contact.tags.add(i)
            tags_id=[tags.id for tags in tag]
            
            new_tags_id =[]
            for i in tags_id:
                if not i in old_tags:
                    new_tags_id.append(i)
            print(new_tags_id,'..........................new')

            campaign = Campaign.objects.filter(trigger_type__trigger_type="tag", client_campaign=client)
            print(campaign)
            campaign_id=[]
            for j in campaign:
                for k in j.trigger_type['trigger_value']:
                    print(k['id'])
                    if k['id'] in new_tags_id:
                        campaign_id.append(j.id)
            print(campaign_id)
            CampaginActivatToContact.delay(contact.id, campaign_id)


        if time_zone:
            time_zone_obj = TimeZone.objects.filter(id=time_zone).first()
            contact.time_zone = time_zone_obj

        if custom_fields:
            for i in custom_fields:
                contact_custom_fields = CustomFieldsValue.objects.filter(contact_user=contact,custom_field__id=i['id']).first()
                if contact_custom_fields:
                    contact_custom_fields.field_value = i['value']
                    contact_custom_fields.save()
                else:
                    custom_field_obj = CustomFields.objects.get(id=i['id'])
                    custom_field_value = CustomFieldsValue.objects.create(custom_field=custom_field_obj,contact_user=contact,field_value=i['value'])

        contact.save()
        response = {
            'status': True,
            'message': "contact user Edit successfully"
        }
        messages.success(request,'Contact User updated successfully')
        return JsonResponse(response)


class ContactDeleteView(View):

    def get(self, request,id):
        print(id)
        contact = ContactUser.objects.get(id=id)
        client=contact.client
        if contact:
            contact.delete()
            messages.success(request,'Contact deleted successfully')
            return redirect('client-contact',id=client.id)
        return render(request, 'client_contact.html')

    def post(self,request,id):
        contact_id=request.POST.getlist('contact_id[]','')
        contact=ContactUser.objects.filter(id__in=contact_id)
        if contact:
            for i in contact:
                i.delete()
        context={
            'status':True,
            'message':'Deleted contacts successfully'
        }
        if contact.count() > 1:
            messages.success(request,'Contacts deleted successfully')
        else:
            messages.success(request,'Contact deleted successfully')
        return JsonResponse(context)


class TagsWiseFilter(View):

    def get(self,request):
        tag_id=request.GET.get('tag_id','')
        client_id=request.GET.get('client_id','')
        client = Client.objects.get(id=client_id)

        if tag_id:
            contact=ContactUser.objects.filter(client=client,tags__id=tag_id)
        else:
            contact = ContactUser.objects.filter(client=client)

        print(contact)
        return render(request, 'contact_table.html', {'contact': contact})

class ClientUserView(ClientPermissionRequiredMixin,View):
    def get(self, request, id):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        client_user=ClientUser.objects.filter(client_owner=client)
        print(settings.CLIENT_USER_WELCOME_TEMPLATE)
        context={
            'client': client,
            'agency': agency,
            'client_user': client_user,
            'today':datetime.now()
        }
        return render(request, 'client_user_view.html',context)

    def post(self,request,id):
        f_name=request.POST.get('first_name','')
        l_name=request.POST.get('last_name','')
        # password=request.POST.get('password','')
        email=request.POST.get('email','')
        passcode=request.POST.get('passcode','')

        obj=Admin.objects.filter(email=email)

        if obj:
            response={
                'status':'unsuccess',
                'message':'Email already exists'
            }
            return JsonResponse(response)

        client=Client.objects.get(id=id)
        if client.server_passcode==passcode:
            context={
                'status':False,
                'message':'Please change the Server Passcode'
            }
            return JsonResponse(context)
        else:
            client_user_check=ClientUser.objects.filter(client_owner=client,server_passcode=passcode)
            if client_user_check:
                context = {
                    'status': False,
                    'message': 'Please change the Server Passcode'
                }
                return JsonResponse(context)

        client_user=ClientUser.objects.create(first_name=f_name,last_name=l_name,email=email,server_passcode=passcode,client_owner=client)

        # client_user.set_password(password)
        client_user.save()

        dyanmic_data_for_template = {
            'first_name': client_user.first_name,
            'last_name': client_user.last_name,
            'server_passcode' : client_user.server_passcode,
            'client_business_name' : client.business_name,
            'agency_name' : client.aegency.business_name,
            'subject':f"{client.business_name} : {settings.CLIENT_USER_PASSCODE}"
        }
        # print([client.business_name] + ":" + settings.CLIENT_USER_WELCOME_TEMPLATE)
        print(client_user.email)
        try:
            send_templated_email(client_user.email, settings.CLIENT_USER_WELCOME_TEMPLATE, dyanmic_data_for_template)
        except Exception as e:
            print(e)
            print(e.__traceback__)
            pass

        response={
            'status':'True',
            'message':'user created successfull'
        }
        messages.success(request,'Client User created successfully')
        return JsonResponse(response)


class ClientUserEditView(View):

    def get(self,request):
        user_id = request.GET.get('user_id', '')
        user = Client.objects.filter(id=user_id).first()
        if not user:
            user = ClientUser.objects.get(id=user_id)
        res = model_to_dict(user)

        response = {
            'status': True,
            'message': 'user created successfull',
            'user': res,
        }
        return JsonResponse(response)

    def post(self,request):
        print(request.POST)
        f_name = request.POST.get('first_name', '')
        l_name = request.POST.get('last_name', '')
        user_id = request.POST.get('user_id', '')
        passcode = request.POST.get('passcode', '')
        
        user = Client.objects.filter(id=user_id).first()
        if not user:
            # For client user 
            user = ClientUser.objects.get(id=user_id)
            client=user.client_owner
            if client.server_passcode == passcode:
                context = {
                    'status': False,
                    'message': 'Please change the Server Passcode'
                }
                return JsonResponse(context)
            else:
                client_user_check = ClientUser.objects.filter(client_owner=client, server_passcode=passcode).exclude(id=user.id)
                if client_user_check:
                    context = {
                        'status': False,
                        'message': 'Please change the Server Passcode'
                    }
                    return JsonResponse(context)  
        else:
            # For client 
            client_user_check = ClientUser.objects.filter(client_owner=user, server_passcode=passcode)
            if client_user_check:
                context = {
                    'status': False,
                    'message': 'Please change the Server Passcode'
                }
                return JsonResponse(context)
        if f_name:
            user.first_name=f_name
        if l_name:
            user.last_name=l_name

        user.server_passcode=passcode
        user.save()

        response = {
            'status': True,
            'message': 'Profile Updated Successfully',
        }
        messages.success(request,'Client User updated successfully')
        return JsonResponse(response)

class ClientUserDeleteView(LoginRequiredMixin,View):
    login_url = '/admin-login/'

    def get(self, request,id):
        user = ClientUser.objects.get(id=id)
        client_id=user.client_owner.id
        if user:
            user.delete()
            messages.success(request,'User deleted successfully')
        return redirect('client-user',id=client_id)


def ClientUserActiveUser(request):
    # Get the product that user has wished for
    user_id = request.POST['user_id']
    active = request.POST['active']
    user = ClientUser.objects.get(id=user_id)
    domain = (f'http://{user.client_owner.aegency.whitelabeldomian}' if user.client_owner.aegency.host.is_verified else settings.LOCAL_EMAIL) if user.client_owner.aegency.host else settings.LOCAL_EMAIL
    if active == 'True':
        print('yes')
        user.is_active = True
        user.save()
        dyanmic_data_for_template = {
            'link': f'{domain}/client/client-login',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'client_name': user.client_owner.business_name,
            'subject':settings.CLIENT_USER_ACTIVE_SUBJECT
        }
        try:
            send_templated_email(user.email, settings.CLIENT_USER_ACTIVE_TEMPALATE, dyanmic_data_for_template)
        except Exception as e:
            print(e)
            print(e.__traceback__)
            pass
        response = {
            "status": False,
            "id":user_id
        }
        return JsonResponse(response)
    else:
        print('no')
        user.is_active = False
        user.save()
        dyanmic_data_for_template = {
            'link': f'{domain}/client/client-login',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'client_name': user.client_owner.business_name,
            'subject':settings.CLIENT_USER_INACTIVE_SUBJECT
        }
        try:
            send_templated_email(user.email, settings.CLIENT_USER_INACTIVE_TEMPALATE, dyanmic_data_for_template)
        except:
            pass
        response = {
            "status": True,
            "id": user_id
        }
        return JsonResponse(response)



class ClientUserStatusWiseFilter(View):
    def get(self,request,id):
        client = Client.objects.get(id=id)
        client_user = ClientUser.objects.filter(client_owner=client)
        status=request.GET.get('status','')

        if status=="1":
            client_user=client_user.filter(is_active=True)
            print(client_user.count(),"1111111111")

            return render(request,'client_user_table.html',{'client_user':client_user, 'client':client, 'today':datetime.now()})
        elif status=="0":
            client_user = client_user.filter(is_active=False)
            print(client_user.count(),"000000000000")
            return render(request, 'client_user_table.html', {'client_user': client_user})
        else:
            print(client_user.count(),'22222222222')
            return render(request, 'client_user_table.html', {'client_user': client_user, 'client':client, 'today':datetime.now()})

class ContactListDeleteView(View):

    def get(self, request,id):
        print(id)
        contact_list = ContactList.objects.get(id=id)
        client=contact_list.list_owner
        if contact_list:
            contact_list.delete()
            messages.success(request,'Contact list deleted successfully')
            return redirect('client-list',id=client.id)
        return render(request, 'client_contact.html')



class ContactListEditView(View):

    def get(self,request):
        list_id=request.GET.get('list_id','')
        list_obj=ContactList.objects.get(id=list_id)
        ser=ContactListSerializer(list_obj)


        response={
            'status':True,
            'data':ser.data
        }
        return JsonResponse(response)

    def post(self,request):
        contact_id=request.POST.getlist('contact_id[]','')
        list_id=request.POST.get('list_id','')
        name=request.POST.get('list_name','')

        contact_list=ContactList.objects.get(id=list_id)
        if name:
            contact_list.name=name

        if contact_id:
            contact_list.contacts.clear()
            contact=ContactUser.objects.filter(id__in=contact_id)
            for i in contact:
                contact_list.contacts.add(i)

        contact_list.save()

        response={
            'status':True,
            'message':'Profile updated successfully'
        }
        messages.success(request,'Contact List updated successfully')
        return JsonResponse(response)



class ClientPhoneNumberView(ClientPermissionRequiredMixin,View):
    def get(self, request, id):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        client_phone=ClientPhoneNumber.objects.filter(client_phone=client)


        context={
            'client': client,
            'agency': agency,
            'client_phone':client_phone,

        }
        return render(request, 'client_phone_no.html',context)

class ClientPhoneNumberGetView(View):
    def get(self, request, id):
        print(request.GET)
        client = Client.objects.get(id=id)
        phone_type=request.GET.get('phone_type','')
        country_code=request.GET.get('country_code','')
        area_code=request.GET.get('area_code','')
        print(phone_type)
        phone_no_list=[]
        if client.account_sid:
            twi_client=twillio_client(client.account_sid,client.auth_token)
            if area_code:
                if phone_type == "local":
                    print('local')
                    phone_no=twi_client.api.available_phone_numbers(f'{country_code}').local.list(limit=15,area_code=area_code)
                    print(phone_no,'.....................................phone_no')
                    for i in phone_no:
                        phone_no_list.append(i.phone_number)
                elif phone_type == "mobile":
                    print('mobile')
                    phone_no = twi_client.api.available_phone_numbers(f'{country_code}').mobile.list(limit=15,area_code=area_code)
                    for i in phone_no:
                        phone_no_list.append(i.phone_number)
                elif phone_type == "toll-free":
                    print('toll')
                    phone_no = twi_client.api.available_phone_numbers(f'{country_code}').toll_free.list(limit=15,area_code=area_code)
                    for i in phone_no:
                        phone_no_list.append(i.phone_number)
            else:
                if phone_type == "local":
                    print('local')
                    phone_no=twi_client.api.available_phone_numbers(f'{country_code}').local.list(limit=15)
                    for i in phone_no:
                        phone_no_list.append(i.phone_number)
                elif phone_type == "mobile":
                    print('mobile')
                    phone_no = twi_client.api.available_phone_numbers(f'{country_code}').mobile.list(limit=15)
                    for i in phone_no:
                        phone_no_list.append(i.phone_number)
                elif phone_type == "toll-free":
                    print('toll')
                    phone_no = twi_client.api.available_phone_numbers(f'{country_code}').toll_free.list(limit=15)
                    for i in phone_no:
                        phone_no_list.append(i.phone_number)


        if phone_no_list:
            data=json.dumps(phone_no_list)
            context = {
                'status': True,
                'phone_no': phone_no_list,
            }
            return JsonResponse(context)
        context = {
            'status': False,
            'msg': 'No. with this Area Code is not available now',
        }
        return JsonResponse(context)

    def post(self,request,id):
        client=Client.objects.get(id=id)
        phone_type = request.POST.get('phone_type', '')
        country_code = request.POST.get('country_code', '')
        area_code = request.POST.get('area_code', '')
        name = request.POST.get('phone_name', '')
        phone_no = request.POST.getlist('phone_no[]', '')
        print(phone_no)

        if client.account_sid:
            twi_client = twillio_client(client.account_sid,client.auth_token)
            for i in phone_no:
                try:
                    number=twi_client.incoming_phone_numbers.create(phone_number=i)
                    phone_obj=ClientPhoneNumber.objects.create(name=name,client_phone=client,phone_number=i,phone_sid=number.sid,phone_type=phone_type)
                    twi_client.incoming_phone_numbers(f'{phone_obj.phone_sid}').update(sms_url=f"{settings.PHONE_WEBHOOK}")
                except Exception as e:
                    print(e)
                    context = {
                        'status': False,
                        'msg': 'Phone number Created Successfully'
                    }
                    return JsonResponse(context)

        phone_obj1=ClientPhoneNumber.objects.filter(client_phone=client,is_default=True)
        if not phone_obj1:
            phone_obj2 = ClientPhoneNumber.objects.filter(client_phone=client).first()
            phone_obj2.is_default=True
            phone_obj2.save()
        context={
            'status':True,
            'msg':'Phone number Created Successfully'
        }
        messages.success(request,'Phone Number created successfully')
        return JsonResponse(context)


class ClientPhoneNumberDeleteView(View):

    def get(self, request,id):
        print(id)
        contact_phone = ClientPhoneNumber.objects.get(id=id)
        client=contact_phone.client_phone
        if contact_phone:
            try:
                if client.account_sid:
                    twi_client = twillio_client(client.account_sid, client.auth_token)
                    twi_client.incoming_phone_numbers(contact_phone.phone_sid).delete()
            except Exception as e:
                print(e)
                print(e.__traceback__.tb_lineno)
            contact_phone.delete()
            messages.success(request,'Client phone number deleted successfully')
            return redirect('client-phone-view',id=client.id)
        return redirect('client-phone-view',id=client.id)

class ClientPhoneNumberMakeDefultView(View):

    def get(self,request,id):
        phone_no=ClientPhoneNumber.objects.get(id=id)
        phone_obj=ClientPhoneNumber.objects.filter(client_phone=phone_no.client_phone,is_default=True)
        if phone_obj:
            for i in phone_obj:
                i.is_default=False
                i.save()
        phone_no.is_default=True
        phone_no.save()
        return redirect('client-phone-view',id=phone_no.client_phone.id)

class ContactUserCouponView(View):

    def get(self,request,unique_id):
        coupon=ContactUserCoupon.objects.filter(short_url=unique_id).first()
        if coupon:
            serializer=ContactUserCouponSerializer(coupon)
        else:
            coupon=ReferralRewardCouponContactUser.objects.filter(short_url=unique_id).first()
            if coupon:
                serializer=ReferralRewardCouponContactUserSerializer(coupon)
            else:
                return JsonResponse(status=404, data={'status':'false','message':'Page Not Found'})
        print(serializer.data)
        return JsonResponse(serializer.data)



class ServerPasscodeCheckView(View):
    def get(self,request,unique_id):
        coupon = ContactUserCoupon.objects.filter(short_url=unique_id).first()
        if not coupon:
            coupon = ReferralRewardCouponContactUser.objects.filter(short_url=unique_id).first()
        server_passcode=request.GET.get('sever_passcode','')

        if coupon.is_read:
            context = {
                'server': False,
                'message': 'Already Redeemed'
            }
            return JsonResponse(context)
        if not coupon.user_coupon.is_no_end:
            validtime=datetime.utcnow().date()+timedelta(days=1)
            if coupon.user_coupon.valid_to.date() <= validtime:
                context = {
                    'status': False,
                    'message': 'Coupon Expired'
                }
                return JsonResponse(context)


        if server_passcode:
            if not coupon.user.client.server_passcode==server_passcode:
                print(coupon.user.client,'vasdasdasd')
                print(server_passcode,'vasdasdasd')
                client_user=ClientUser.objects.filter(client_owner=coupon.user.client,server_passcode=server_passcode)
                print(client_user)
                if not client_user:
                    context={
                        'server':False,
                        'message':'The Server Passcode is Invalid'
                    }
                    return JsonResponse(context)

        context = {
            'status': True,
            'message': 'done'
        }
        return JsonResponse(context)

class CouponReedemView(View):

    def get(self,request,unique_id):
        coupon = ContactUserCoupon.objects.filter(short_url=unique_id).first()

        if not coupon:
            coupon = ReferralRewardCouponContactUser.objects.filter(short_url=unique_id).first()

        server_passcode = request.GET.get('sever_passcode', '')
        amount = request.GET.get('amount', '')

        if coupon.is_read:
            context = {
                'server': False,
                'message': 'The Coupon is already reedemed'
            }
            return JsonResponse(context)
        if not coupon.user_coupon.is_no_end:
            validtime=datetime.utcnow().date()
            if coupon.user_coupon.valid_to:
                if validtime > coupon.user_coupon.valid_to.date():
                    context = {
                        'status': False,
                        'message': 'The Server Passcode is Invalid'
                    }
                    return JsonResponse(context)



        if not coupon.user.client.server_passcode==server_passcode:
            print(coupon.user.client,'vasdasdasd')
            print(server_passcode,'vasdasdasd')
            client_user=ClientUser.objects.filter(client_owner=coupon.user.client,server_passcode=server_passcode)
            print(client_user)
            if not client_user:
                context={
                    'server':False,
                    'message':'The Server Passcode is Invalid'
                }
                return JsonResponse(context)

        print(amount)
        coupon_obj=Coupon.objects.get(id=coupon.user_coupon.id)
        user_obj=ContactUser.objects.get(id=coupon.user.id)
        if not coupon.amount:
            coupon.amount=float(amount)
        else:
            coupon.amount += float(amount)

        coupon.is_read=True
        coupon.updated_at=datetime.utcnow()
        coupon.save()

        if not coupon_obj.is_read_count:
            coupon_obj.is_read_count=1
        else:
            coupon_obj.is_read_count += 1
        if not coupon_obj.sales:
            coupon_obj.sales=float(amount)
        else:
            coupon_obj.sales += float(amount)
        coupon_obj.save()

        if not user_obj.sales:
            user_obj.sales=float(amount)
        else:
            user_obj.sales += float(amount)
        user_obj.save()

        # For Referral Coupon 
        contact_referral = ReferralCampaignToContact.objects.filter(referral_camp__ref_coupon=coupon.user_coupon,refered_user=coupon.user).first()
        if contact_referral:
            contact = contact_referral.contact_user
            reward_coupon = contact_referral.referral_camp.reward_coupon

            client = Client.objects.get(id=contact.client.id)
            client_phone_no = ClientPhoneNumber.objects.filter(client_phone=client,is_default=True).first()

            referral_camp = ReferralCampaigns.objects.filter(id=contact_referral.referral_camp.id).first()
            if not referral_camp.is_read_count:
                referral_camp.is_read_count = 1
            else:
                referral_camp.is_read_count = int(referral_camp.is_read_count) + 1
            referral_camp.save()

            exist_user_coupon = ContactUserCoupon.objects.filter(user=contact, user_coupon=reward_coupon).first()
            if not exist_user_coupon:
                user_coupon = ContactUserCoupon.objects.create(user=contact, user_coupon=reward_coupon)
            else:
                coup = Coupon.objects.get(id=reward_coupon.id)

                user_coupon = ReferralRewardCouponContactUser.objects.create(user=contact,user_coupon=coup,new_user=user_obj)

                # prifix_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                # new_coup_name = f'{coup.coupon_name}_{prifix_name}'
                # coupon_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
                # coupon_code_check=get_unique_coupon_code(coupon_code,client)

                # new_coupon = Coupon.objects.create(coupon_name=new_coup_name,discount_type=coup.discount_type,discount_value=coup.discount_value,minmum_spend=coup.minmum_spend,coupon_code=coupon_code_check,is_referral=True,client_coupon=client,is_referral_reward=True)
                # user_coupon = ContactUserCoupon.objects.create(user=contact, user_coupon=new_coupon)

            break_line = '\n'
            message = f"{client.business_name}: Congratulations! You've had a successful referral. Here is your reward voucher: {settings.COUPON_URL}{user_coupon.short_url} {break_line}We appreciate your support."
            OneToOneMessage.objects.create(message=message,contact=contact,client=client,is_send=True)

            try:
                if client.account_sid:
                    twi_client = twillio_client(client.account_sid, client.auth_token)
                    message_obj = twi_client.messages.create(to=f'{contact.phone_no}',
                                                        from_=f'{client_phone_no.phone_number}',
                                                        body=message)
            except Exception as e:
                print(e)
                print(e.__traceback__.tb_lineno)

        return JsonResponse({'status':True,'message':'done'})


class CongratulationView(View):

    def get(self,request,unique_id):
        coupon=ContactUserCoupon.objects.get(short_url=unique_id)

        serializer=ContactUserCouponSerializer(coupon)
        print(serializer.data)
        return JsonResponse(serializer.data)


class ContactUserUpdateView(View):

    def get(self,request,unique_id):
        coupon = ContactUserCoupon.objects.filter(short_url=unique_id).first()

        if not coupon:
            coupon = ReferralRewardCouponContactUser.objects.filter(short_url=unique_id).first()
            if not coupon:
                return JsonResponse(status=404, data={'status':'false','message':'Page Not Found'})

        birth_date = request.GET.get('birth', '')
        name = request.GET.get('name', '')

        user=ContactUser.objects.get(id=coupon.user.id)
        if birth_date:
            user.birthday=birth_date

        if name and name != "None":
            user.first_name=name

        user.save()
        return JsonResponse({'status':True,'msg':'Done'})


class ScheduleCron(View):
    def get(self,request):
        ScheduleToSentBroadcast.delay()
        return redirect('client-login')

class SmartListCron(View):
    def get(self,request):
        SmartList.delay()
        return redirect('client-login')

class CouponExpireCron(View):
    def get(self,request):
        CouponValidation.delay()
        return redirect('client-login')

class CampaignStartForDateBased(View):
    def get(self,request):
        CampaignStartForDateBasedTrigger.delay()
        return redirect('client-login')

class RemoveCampaign(View):
    def get(self,request):
        RemoveComplateCampaign.delay()
        return redirect('client-login')

class SendReferralCouponToContact(View):
    def get(self, request):
        SendReferralCouponToContactUser.delay()
        return redirect('client-login')

class CampaignsCreationView(ClientPermissionRequiredMixin,View):

    def get(self,request,id):
        client=Client.objects.get(id=id)
        client_phone=ClientPhoneNumber.objects.filter(client_phone=client)
        campaign_name=f'Campaign {datetime.now().strftime("%Y-%m-%d TO %H:%M")}'
        tags=Tags.objects.filter(client_tag=client)
        day=Days.objects.all().order_by('id')
        coupon=Coupon.objects.filter(client_coupon=client,is_valid=True,is_referral=False)
        custom_fields=CustomFields.objects.filter(client_field=client)
        referral_camp = ReferralCampaigns.objects.filter(client_rc=client)


        if not client_phone:
            messages.error(request,"To use campaigns you must first purchase a phone number")
            return redirect('client-campaigns',id=id)

        context={
            'client':client,
            'client_phone':client_phone,
            'campaign_name':campaign_name,
            'tags':tags,
            'days':day,
            'time':range(1,13),
            'coupon':coupon,
            'hours': range(1, 13),
            'minute': range(60),
            'before_days' : range(1,11),
            'custom_fields' : custom_fields,
            'referral_camp': referral_camp,
        }
        return render(request,'campaign_creation.html',context)


    def post(self,request,id):
        client = Client.objects.get(id=id)
        print(request.POST)
        keyword_phone=request.POST.get('keyword_phone','')
        keyword=request.POST.get('keyword','')
        name=request.POST.get('campaign_form_name','')
        datebased=request.POST.getlist('datebased_trigger','')
        tags=request.POST.getlist('tag_based','')
        send_check=request.POST.get('send_check','')
        days=request.POST.getlist('days','')
        start_time=request.POST.get('start_time','')
        end_time=request.POST.get('end_time','')
        send_number=request.POST.get('send_number','')
        double_keyword=request.POST.get('double_keyword','')
        double_optin=request.POST.get('double_optin','')
        limit_multiple=request.POST.get('limit_multiple','')
        double_message=request.POST.get('double_message','')
        limit_message=request.POST.get('limit_message','')
        cancel_trigger=request.POST.get('cancel_trigger','')
        on_reply=request.POST.get('on_reply','')
        cancel_tag=request.POST.get('cancel_tag','')
        cancel_message=request.POST.get('cancel_message','')
        cancel_keyword=request.POST.get('cancel_keyword','')
        cancel_tag_based=request.POST.get('cancel_tag_based','')
        message=request.POST.get('message','')
        order=request.POST.get('order','')
        minute=request.POST.get('minute','')
        hour=request.POST.get('hour','')
        time_am=request.POST.get('time_am','')
        time=request.POST.get('time','')
        time_val=request.POST.get('time_val','')
        tag_action = request.POST.getlist('tag_action','')
        before_days=request.POST.get('before_days','')
        print(before_days)
        if not before_days:
            before_days = 0

        campaign=Campaign.objects.create(name=name,client_campaign=client)
        days_objcets=Days.objects.filter(is_defualt=True)
        client_phone=ClientPhoneNumber.objects.filter(client_phone=client,is_default=True).first()

        if client_phone:
            campaign.send_phone=client_phone
        if keyword_phone:
            phone=ClientPhoneNumber.objects.get(id=keyword_phone)
            campaign.keyword_phone=phone
        if keyword:
            campaign.keyword_value=keyword
        if datebased:
            temp_dict={
                'trigger_type':"date",
                'trigger_value':{'date_based':datebased,'before_days':int(before_days)}
            }
            campaign.is_sending = False
            campaign.trigger_type=temp_dict

        if tags:
            tags_obj=Tags.objects.filter(id__in=tags)
            ser=TagsSerializer(tags_obj,many=True)
            temp_dict = {
                'trigger_type': "tag",
                'trigger_value': ser.data
            }
            campaign.trigger_type = temp_dict

        if send_check:
            campaign.is_sending=True
            if days:
                day_objs=Days.objects.filter(id__in=days)
                if day_objs:
                    campaign.sending_days.add(*day_objs)
            if start_time:
                start=datetime.strptime(start_time,"%I-%p")
                campaign.start_time=start.time()
            if end_time:
                end=datetime.strptime(end_time,"%I-%p")
                campaign.end_time=end.time()

        if send_number:
            client_phone = ClientPhoneNumber.objects.get(id=send_number)
            campaign.send_phone=client_phone
        if double_optin:
            campaign.is_double=True
            if double_keyword:
                campaign.double_keyword=double_keyword
            if double_message:
                campaign.double_message=double_message
        if limit_multiple:
            campaign.is_limit=True
            if limit_message:
                campaign.limit_message=limit_message
        if cancel_trigger:
            campaign.is_cancel=True
            if on_reply:
                campaign.on_reply=True

        if not send_check:
            if days_objcets:
                campaign.sending_days.add(*days_objcets)

        if message:
            cam_action=CampaignAction.objects.create(campaign_action=campaign)
            temp_a={
                'action_type':'text_message',
                'action_value':message
            }
            cam_action.action=temp_a
            cam_action.order=int(order)+1
            cam_action.save()

        if hour:
            cam_action = CampaignAction.objects.create(campaign_action=campaign)
            temp_a = {
                'action_type': 'wait_until',
                'action_value': {'hour':hour,'minute':minute,'time_am':time_am}
            }
            cam_action.action = temp_a
            cam_action.order = int(order) + 1
            cam_action.save()
        if time:
            cam_action = CampaignAction.objects.create(campaign_action=campaign)
            temp_a = {
                'action_type': 'time_delay',
                'action_value': {'time':time,'time_val':time_val}
            }
            cam_action.action = temp_a
            cam_action.order = int(order) + 1
            cam_action.save()

        if tag_action:
            tag = Tags.objects.filter(id__in=tag_action)
            ser = TagsSerializer(tag, many=True)
            cam_action = CampaignAction.objects.create(campaign_action=campaign)
            temp_a = {
                'action_type': 'tag_action',
                'action_value': ser.data
            }
            cam_action.action = temp_a
            cam_action.order = int(order) + 1
            cam_action.save()

        campaign.save()
        return redirect('campaign-edit',id=campaign.id)



class CampaignsEditView(View):

    def get(self,request,id):
        campaign=Campaign.objects.get(id=id)
        cam_action=CampaignAction.objects.filter(campaign_action=campaign).order_by('order')
        client=campaign.client_campaign
        client_phone = ClientPhoneNumber.objects.filter(client_phone=client)
        tags=Tags.objects.filter(client_tag=client)
        day = Days.objects.all().order_by('id')
        coupon=Coupon.objects.filter(client_coupon=client,is_valid=True,is_referral=False)
        custom_fields=CustomFields.objects.filter(client_field=client)
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        referral_camp = ReferralCampaigns.objects.filter(client_rc=client)


        context={
            'client':client,
            'agency': agency,
            'client_phone':client_phone,
            'campaign':campaign,
            'tags':tags,
            'days': day,
            'time': range(1, 13),
            'cam_actions':cam_action,
            'hours': range(1, 13),
            'minute': range(60),
            'coupon':coupon,
            'before_days' : range(1,11),
            'custom_fields' : custom_fields,
            'referral_camp': referral_camp,
        }
        return render(request,'campaign_creation_edit.html',context)

    def post(self,request,id):
        campaign = Campaign.objects.get(id=id)
        name = request.POST.get('campaign_form_name', '')
        send_check=request.POST.get('send_check','')
        days=request.POST.getlist('days','')
        start_time=request.POST.get('start_time','')
        end_time=request.POST.get('end_time','')
        send_number=request.POST.get('send_number','')
        double_keyword=request.POST.get('double_keyword','')
        double_optin=request.POST.get('double_optin','')
        limit_multiple=request.POST.get('limit_multiple','')
        double_message=request.POST.get('double_message','')
        limit_message=request.POST.get('limit_message','')
        cancel_trigger=request.POST.get('cancel_trigger','')
        on_reply=request.POST.get('on_reply','')
        cancel_tag=request.POST.get('cancel_tag','')
        cancel_message=request.POST.get('cancel_message','')
        cancel_keyword=request.POST.get('cancel_keyword','')
        cancel_tag_based=request.POST.get('cancel_tag_based','')


        if name:
            campaign.name=name
        if not send_check:
            campaign.is_sending = False
        if send_check:
            campaign.is_sending=True
            if days:
                campaign.sending_days.clear()
                day_objs=Days.objects.filter(id__in=days)
                if day_objs:
                    campaign.sending_days.add(*day_objs)
            if start_time:
                start=datetime.strptime(start_time,"%I-%p")
                print(start.time())
                campaign.start_time=start.time()
            if end_time:
                end=datetime.strptime(end_time,"%I-%p")
                print(end.time())
                campaign.end_time=end.time()

        if send_number:
            client_phone = ClientPhoneNumber.objects.get(id=send_number)
            campaign.send_phone=client_phone
        if double_optin:
            campaign.is_double=True
            if double_keyword:
                campaign.double_keyword=double_keyword
            if double_message:
                campaign.double_message=double_message
        else:
            campaign.is_double = False
            campaign.double_keyword = ''
            campaign.double_message = ''
        if limit_multiple:
            campaign.is_limit=True
            if limit_message:
                campaign.limit_message=limit_message
        else:
            campaign.is_limit = False
            campaign.limit_message=''
        if cancel_trigger:
            campaign.is_cancel=True
            if on_reply:
                campaign.on_reply=True

        else:
            campaign.is_cancel = False
            campaign.on_reply = False

        campaign.save()
        return redirect('campaign-edit',id=campaign.id)


class CampaignsDeleteView(View):

    def get(self, request,id):
        print(id)
        campaign = Campaign.objects.get(id=id)
        client=campaign.client_campaign
        if campaign:
            campaign.delete()
            messages.success(request,'Campaign deleted successfully')
            return redirect('client-campaigns',id=client.id)
        return render(request, 'coupon.html')

class CampaignsActionCreateView(View):

    def post(self, request, id):
        campaign = Campaign.objects.get(id=id)
        print(request.POST)
        message=request.POST.get('message','')
        order=request.POST.get('order','')
        minute=request.POST.get('minute','')
        hour=request.POST.get('hour','')
        time_am=request.POST.get('time_am','')
        time=request.POST.get('time','')
        time_val=request.POST.get('time_val','')
        tag_action = request.POST.getlist('tag_action','')
        keyword=request.POST.get('keyword','')
        keyword_phone=request.POST.get('keyword_phone','')
        datebased=request.POST.getlist('datebased_trigger','')
        tags=request.POST.getlist('tag_based','')
        before_days=request.POST.get('before_days','')
        print(before_days)
        if not before_days:
            before_days = 0

        if keyword:
            campaign.keyword_value=keyword
            campaign.save()

        if keyword_phone:
            phone=ClientPhoneNumber.objects.get(id=keyword_phone)
            campaign.keyword_phone=phone
            campaign.save()

        if datebased:
            temp_dict={
                'trigger_type':"date",
                'trigger_value':{'date_based':datebased,'before_days':int(before_days)}
            }
            campaign.trigger_type=temp_dict
            campaign.is_sending = False
            campaign.save()

        if tags:
            tags_obj=Tags.objects.filter(id__in=tags)
            ser=TagsSerializer(tags_obj,many=True)
            temp_dict = {
                'trigger_type': "tag",
                'trigger_value': ser.data
            }
            campaign.trigger_type = temp_dict
            campaign.save()

        if order:
            cam_action = CampaignAction.objects.filter(campaign_action=campaign,order__gt=order)
            print(cam_action)

            if cam_action:
                for i in cam_action:
                    print(i.order,'************')
                    i.order += 1
                    i.save()

        if message:
            cam_action=CampaignAction.objects.create(campaign_action=campaign)
            temp_a={
                'action_type':'text_message',
                'action_value':message
            }
            cam_action.action=temp_a
            cam_action.order=int(order)+1
            cam_action.save()

        if hour:
            cam_action = CampaignAction.objects.create(campaign_action=campaign)
            temp_a = {
                'action_type': 'wait_until',
                'action_value': {'hour':hour,'minute':minute,'time_am':time_am}
            }
            cam_action.action = temp_a
            cam_action.order = int(order) + 1
            cam_action.save()

        if time:
            cam_action = CampaignAction.objects.create(campaign_action=campaign)
            temp_a = {
                'action_type': 'time_delay',
                'action_value': {'time':time,'time_val':time_val}
            }
            cam_action.action = temp_a
            cam_action.order = int(order) + 1
            cam_action.save()

        if tag_action:
            tag = Tags.objects.filter(id__in=tag_action)
            ser = TagsSerializer(tag, many=True)
            cam_action = CampaignAction.objects.create(campaign_action=campaign)
            temp_a = {
                'action_type': 'tag_action',
                'action_value': ser.data
            }
            cam_action.action = temp_a
            cam_action.order = int(order) + 1
            cam_action.save()
        return redirect('campaign-edit',id=campaign.id)

class CampaignsActionEditView(View):

    def post(self, request):
        print(request.POST)
        id = request.POST.get('cam_action_id','')
        print(id)
        message=request.POST.get('message','')
        order=request.POST.get('order','')
        minute=request.POST.get('minute','')
        hour=request.POST.get('hour','')
        time_am=request.POST.get('time_am','')
        time=request.POST.get('time','')
        time_val=request.POST.get('time_val','')
        tag_action = request.POST.getlist('tag_action','')
        cam_action = CampaignAction.objects.get(id=id)
        print(cam_action)

        if message:
            temp_a={
                'action_type':'text_message',
                'action_value':message
            }
            cam_action.action = temp_a
            cam_action.save()

        if hour:
            temp_a = {
                'action_type': 'wait_until',
                'action_value': {'hour':hour,'minute':minute,'time_am':time_am}
            }
            cam_action.action = temp_a
            cam_action.save()

        if time:
            temp_a = {
                'action_type': 'time_delay',
                'action_value': {'time':time,'time_val':time_val}
            }
            cam_action.action = temp_a
            cam_action.save()

        if tag_action:
            tag = Tags.objects.filter(id__in=tag_action)
            ser = TagsSerializer(tag, many=True)
            temp_a = {
                'action_type': 'tag_action',
                'action_value': ser.data
            }
            cam_action.action = temp_a
            cam_action.save()
        return redirect('campaign-edit',id=cam_action.campaign_action.id)

class CampaignsEditGetDataView(View):
    def get(self, request, id):
        cam_action = CampaignAction.objects.get(id=id)
        res = model_to_dict(cam_action)
        return JsonResponse({'status':True,'msg':'Done', 'data':res})

class CampaignsActionDeleteView(View):
    def get(self, request, id):
        cam_action_obj = CampaignAction.objects.get(id=id)
        cam_action = CampaignAction.objects.filter(campaign_action=cam_action_obj.campaign_action,order__gt=cam_action_obj.order)
        cam_id = cam_action_obj.campaign_action.id
        cam_action_obj.delete()

        if cam_action:
            for i in cam_action:
                i.order -= 1
                i.save()

        messages.success(request,"Trigger deleted successfully")
        return redirect('campaign-edit',id=cam_id)

class CampaignStartView(View):
    def post(self, request):
        contact_id = request.POST.get('contact_id','')
        campaign_id = request.POST.getlist('campaign_id[]','')
        print(contact_id)
        print(campaign_id)
        CampaginActivatToContact.delay(contact_id,campaign_id)
        messages.success(request,"Contact added to Campaign successfully")
        return JsonResponse({'status':True,'msg':'Done'})


class SetPhoneNumberWebhook(View):
    def get(self,request):
        # phone=ClientPhoneNumber.objects.all()
        #
        # for i in phone:
        #     if i.client_phone.account_sid:
        #         twi_client = twillio_client(i.client_phone.account_sid, i.client_phone.auth_token)
        #
        #         try:
        #             twi_client.incoming_phone_numbers(f'{i.phone_sid}').update(sms_url=f"{settings.PHONE_WEBHOOK}")
        #         except Exception as e:
        #             print(e)
        #             print(e.__traceback__.tb_lineno)
        client=Client.objects.all()
        for i in client:
            if i.message_service_id:
                if i.account_sid:
                    twi_client = twillio_client(i.account_sid, i.auth_token)

                    try:
                        twi_client.messaging.services(f'{i.message_service_id}').update(inbound_request_url=f'{settings.PHONE_WEBHOOK}')
                    except Exception as e:
                        print(e)
                        print(e.__traceback__.tb_lineno)
        return redirect('client-login')

@csrf_exempt
def handle_incoming_message(request):
    from_no=request.POST.get('From','') # ContactUser
    to_number=request.POST.get('To','') # ClientPhoneNumber
    message=request.POST.get('Body','')
    print(from_no,'from_no')
    print(to_number)
    to_no=ClientPhoneNumber.objects.filter(phone_number=to_number).first()
    if to_no:
        from_no_obj=ContactUser.objects.filter(phone_no=from_no,client=to_no.client_phone).first()
        if not from_no_obj:
            from_no_obj=ContactUser.objects.create(phone_no=from_no,client=to_no.client_phone)

        
        obj = OneToOneMessage.objects.create(message=message,contact=from_no_obj,client=to_no.client_phone,is_receive=True)
        print(obj.__dict__,'.............................')
        campaign=Campaign.objects.all()
        if campaign:
            double_optin_cam=campaign.filter(is_double=True,double_keyword__iexact=message)
            if double_optin_cam:
                double_campaign_id=[]
                for cam in double_optin_cam:
                    double_cam= DoubleOptinCampaign.objects.filter(contact_user=from_no_obj,campagin=cam)
                    if double_cam:
                        double_campaign_id.append(cam.id)
                        double_cam.delete()
                CampaginActivatToContact.delay(from_no_obj.id, double_campaign_id)
            key_campaign=campaign.filter(keyword_phone=to_no)
            print(key_campaign)
            if key_campaign:
                print('yes')
                key_campaign_id=[]
                for i in key_campaign:
                    if i.keyword_value.lower() in message.lower():
                        if i.is_double:
                            DoubleOptinCampaign.objects.create(contact_user=from_no_obj,campagin=i)
                            CampaignActionForTextMessage.delay(i.double_message,to_no.client_phone.id,f"{from_no_obj.phone_no}",f"{to_no.phone_number}")
                        else:
                            key_campaign_id.append(i.id)
                CampaginActivatToContact.delay(from_no_obj.id, key_campaign_id)
            cancel_campaign=campaign.filter(send_phone=to_no,is_cancel=True,on_reply=True)
            if cancel_campaign:
                cancel_campaign_id=[i.id for i in cancel_campaign]
                CancelationTrigger(cancel_campaign_id,from_no_obj.id)

    return HttpResponse({'status':True,'msg':'done'},content_type='application/xml')


class ClientListBroadcastView(View):
    def get(self, request, id):
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        list=ContactList.objects.get(id=id)
        client = Client.objects.get(first_name=list.list_owner)
        client_list = ContactList.objects.filter(list_owner=client)
        contact_count=ContactUser.objects.filter(client=client).count()
        coupon=Coupon.objects.filter(client_coupon=client,is_valid=True,is_referral=False)
        context={
            'client': client,
            'agency': agency,
            'contact_count':contact_count,
            'list':list,
            'client_list':client_list,
            'coupon':coupon,
            'hours':range(1,13),
            'minute':range(60),
        }
        return render(request, 'client_scheduled_broadcast.html', context)



class ClientPhoneNoFilter(View):
    def get(self, request):
        id = request.GET.get('id','')
        type = request.GET.get('type','')
        client = Client.objects.get(id=id)

        if type == "Local" or type == "Mobile" or type == "Toll-free":
            client_phone=ClientPhoneNumber.objects.filter(client_phone=client,phone_type__icontains=type)
        if type == "Type":    
            client_phone=ClientPhoneNumber.objects.filter(client_phone=client)
        print(client_phone)

        context={
            'client': client,
            'client_phone':client_phone,

        }
        return render(request, 'client_phone_no_filter.html',context)

class GetListsForContactView(View):
    def get(self, request):
        client_id = request.GET.get('client_id','')
        contact_id = request.GET.get('contact_id','')
        client = Client.objects.get(id=client_id)
        contact=ContactUser.objects.filter(client=client,id=contact_id)
        contact_list=ContactList.objects.filter(list_owner=client).exclude(contacts__in=contact)
        context = {
            'list' :contact_list,
        }
        return render(request, 'contact_list_table.html',context)


class AddContactToListView(View):
    def post(self, request):
        client_id = request.POST.get('client_id','')
        contact_id = request.POST.get('contact_id','')
        list_id = request.POST.getlist('list_id[]','')
        client = Client.objects.get(id=client_id)
        contact=ContactUser.objects.get(client=client,id=contact_id)
        contact_list=ContactList.objects.filter(list_owner=client,id__in=list_id)

        for i in contact_list:
            print(i)
            i.contacts.add(contact)

        messages.success(request,"Contact added to List successfully")
        return JsonResponse({'status':True,'msg':'Done'})


class AddCustomFieldsView(View):
    def get(self, request, id):
        # client_id = request.GET.get('client_id','')
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        custom_fields = CustomFields.objects.filter(client_field=client)
        context = {
            'client': client,
            'custom_fields': custom_fields,
            'agency':agency
        }
        return render(request, 'client_custom_fields.html', context)

    def post(self, request, id):
        client_id = request.POST.get('client_id','')
        field_name = request.POST.get('field_name','')
        placeholder_name = request.POST.get('placeholder_name','')
        field_type = request.POST.get('field_type','')
        client = Client.objects.get(id=client_id)
        try:
            field = CustomFields.objects.filter(client_field=client,field_name__iexact=field_name)
            if not field:
                custom_field = CustomFields.objects.create(field_name=field_name,field_placeholder=placeholder_name,field_type=field_type,client_field=client)
                messages.success(request,"Field added successfully")
            else:
                messages.error(request,"Field name already exists")
        except:
            messages.error(request,"Field name already exists")
        return JsonResponse({'status':True,'msg':'Done'})


class EditCustomFieldView(View):
    def get(self, request):
        field_id = request.GET.get('field_id','')
        field = CustomFields.objects.get(id=field_id)
        print(field)
        field = model_to_dict(field)
        return JsonResponse({'status':True,'msg':'Done','data':field})

    def post(self, request):
        field_id = request.POST.get('field_id','')
        field_name = request.POST.get('field_name','')
        placeholder_name = request.POST.get('placeholder_name','')
        field = CustomFields.objects.get(id=field_id)

        field.field_name = field_name
        field.field_placeholder = placeholder_name
        field.save()
        messages.success(request,"Field edited successfully")
        return JsonResponse({'status':True,'msg':'Done'})


class DeleteCustomFieldView(View):
    def get(self, request):
        field_id = request.GET.get('field_id','')
        field = CustomFields.objects.get(id=field_id)
        print(field)
        field.delete()
        messages.success(request,'Field deleted successfully')
        return JsonResponse({'status':True,'msg':'Done'})

class ClientTagsView(View):
    def get(self, request, id):
        # client_id = request.GET.get('client_id','')
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        client = Client.objects.get(id=id)
        tags = Tags.objects.filter(client_tag=client)
        context = {
            'client': client,
            'tags': tags,
            'agency':agency
        }
        return render(request, 'client_tags.html', context)

    def post(self, request, id):
        client_id = request.POST.get('client_id','')
        tag_name = request.POST.get('tag_name','')
        print(tag_name,'asfdghas')

        client = Client.objects.get(id=client_id)
        try:
            tag = Tags.objects.filter(client_tag=client,name__iexact=tag_name)
            if not tag:
                custom_field = Tags.objects.create(name=tag_name,client_tag=client)
                messages.success(request,"Tag added successfully")
            else:
                return JsonResponse({'status': False, 'msg': 'Tag name already exists'})

        except:
            return JsonResponse({'status': False, 'msg': 'Tag name already exists'})
        return JsonResponse({'status':True,'msg':'Done'})



class EditTagView(View):
    def get(self, request):
        print(request.GET)
        tag_id = request.GET.get('tag_id','')
        print(tag_id)
        tag = Tags.objects.get(id=tag_id)
        print(tag)
        tag_data = model_to_dict(tag)
        return JsonResponse({'status':True,'msg':'Done','data':tag_data})

    def post(self, request):
        print(request.POST)
        tag_id = request.POST.get('tag_id','')
        print(type(tag_id))
        tag_name = request.POST.get('tag_name','')
        tag = Tags.objects.get(id=tag_id)

        tag_exist = Tags.objects.filter(client_tag=tag.client_tag,name__iexact=tag_name).exclude(id=tag_id)
        print(tag_exist)

        if tag_exist:
            return JsonResponse({'status':False,'msg':'Tag name already exists'})
        
        tag.name = tag_name
        tag.save()
        messages.success(request,"Tag updated successfully")
        return JsonResponse({'status':True,'msg':'Done'})


class DeleteTagView(View):
    def get(self, request,id):
        tag = Tags.objects.get(id=id)
        client=tag.client_tag
        tag.delete()
        messages.success(request,'Tag deleted successfully')
        return redirect('client-tag-view',id=client.id)

class GetChatHistory(View):
    def get(self, request):
        client_id = request.GET.get('client_id','')
        contact_id = request.GET.get('contact_id','')

        client = Client.objects.filter(id=client_id).first()
        contact = ContactUser.objects.filter(id=contact_id,client=client).first()

        messages = OneToOneMessage.objects.filter(client=client,contact=contact).order_by('created_at')

        context = {
            'contact' : contact,
            'messages' : messages,
        }

        return render(request, 'chat_history.html', context)

class ChatSystem(View):
    def post(self, request):
        client_id = request.POST.get('client_id','')
        contact_id = request.POST.get('contact_id','')
        message = request.POST.get('message','')

        client = Client.objects.filter(id=client_id).first()
        client_phone_no = ClientPhoneNumber.objects.filter(client_phone=client,is_default=True).first()
        contact = ContactUser.objects.filter(id=contact_id,client=client).first()

        OneToOneMessage.objects.create(message=message,contact=contact,client=client,is_send=True)
        try:
            if client.account_sid:
                twi_client = twillio_client(client.account_sid, client.auth_token)
                message_obj = twi_client.messages.create(to=f'{contact.phone_no}',
                                                     from_=f'{client_phone_no.phone_number}',
                                                     body=message)
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_lineno)

        messages = OneToOneMessage.objects.filter(client=client,contact=contact).order_by('created_at')

        context = {
            'contact' : contact,
            'messages' : messages,
        }

        return render(request, 'chat_history.html', context)


class ClientReferralCampaignListView(View):
    def get(self, request, id):
        client = Client.objects.get(id=id)
        agency = AgencyUser.objects.filter(id=request.user.id).first()
        referral_camps = ReferralCampaigns.objects.filter(client_rc=client).annotate(total=Coalesce(F('ref_coupon__sales'),float(0)) + Coalesce(F('reward_coupon__sales'),float(0)))
        context = {
            "client" : client,
            'agency' : agency,
            'referral_camps':referral_camps,
        }
        return render(request, "client_referral_campaign.html", context)

    def post(self, request, id):
        client = Client.objects.get(id=id)
        name=request.POST.get('name','')
        dis_type=request.POST.get('dis_type','')
        dis_value=request.POST.get('dis_value','')
        spend=request.POST.get('spend','')
        reward_type=request.POST.get('reward_type','')
        reward_value=request.POST.get('reward_value','')

        if dis_type == "1":
            coupon_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            coupon_code_check=get_unique_coupon_code(coupon_code,client)
            dis_coupon=Coupon.objects.create(coupon_name=name,discount_type='percentage',discount_value=dis_value,minmum_spend=spend,coupon_code=coupon_code_check,is_referral=True,client_coupon=client,is_referral_dis=True)
        elif dis_type == "2":
            coupon_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            coupon_code_check=get_unique_coupon_code(coupon_code,client)
            dis_coupon=Coupon.objects.create(coupon_name=name,discount_type='rs',discount_value=dis_value,minmum_spend=spend,coupon_code=coupon_code_check,is_referral=True,client_coupon=client,is_referral_dis=True)

        if reward_type == "1":
            coupon_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            coupon_code_check=get_unique_coupon_code(coupon_code,client)
            rew_coupon=Coupon.objects.create(coupon_name=name,discount_type='percentage',discount_value=reward_value,minmum_spend=spend,coupon_code=coupon_code_check,is_referral=True,client_coupon=client,is_referral_reward=True)
        elif reward_type == "2":
            coupon_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            coupon_code_check=get_unique_coupon_code(coupon_code,client)
            rew_coupon=Coupon.objects.create(coupon_name=name,discount_type='rs',discount_value=reward_value,minmum_spend=spend,coupon_code=coupon_code_check,is_referral=True,client_coupon=client,is_referral_reward=True)

        referral_camp = ReferralCampaigns.objects.create(ref_camp_name=name,ref_coupon=dis_coupon,reward_coupon=rew_coupon,client_rc=client)

        context={
            'status':True,
        }
        messages.success(request,'Referral campaign created successfully')
        return JsonResponse(context)

class ReferralCampaignDeleteView(View):
    def get(self, request, id):
        referral_camp = ReferralCampaigns.objects.get(id=id)
        if referral_camp:
            client = referral_camp.client_rc
            ref_coupon = referral_camp.ref_coupon
            reward_coupon = referral_camp.reward_coupon
            ref_c = Coupon.objects.filter(id=ref_coupon.id).first()
            if ref_c:
                ref_c.delete()
            reward_c = Coupon.objects.filter(id=reward_coupon.id).first()
            if reward_c:
                reward_c.delete()
            referral_camp.delete()
            messages.success(request,'Referral campaign deleted successfully')
            return redirect('client-referral-campaign',id=client.id)
        return render(request, 'client_referral_campaign.html')
        
class GetContactReferralCampaignData(View):
    def get(self, request, unique_id):
        contact_referral = ReferralCampaignToContact.objects.filter(short_url=unique_id).first()
        if not contact_referral:
            return JsonResponse(status=404, data={'status':'false','message':'Page Not Found'})
        
        serializer = ContactUserReferralCampaignSerializer(contact_referral)
        # print(serializer.data)
        return JsonResponse(serializer.data)

class AddClaimVoucherContactUser(View):
    def get(self, request, unique_id):
        country_code = request.GET.get('country_code','')
        country_name = request.GET.get('country_name','')
        number = request.GET.get('number','')
        phone_number=f'{country_code}{number}'
        
        contact_referral = ReferralCampaignToContact.objects.get(short_url=unique_id)
        client = Client.objects.get(id=contact_referral.referral_camp.client_rc.id)
        client_phone_no = ClientPhoneNumber.objects.filter(client_phone=client,is_default=True).first()

        contact_user = ContactUser.objects.filter(phone_no=phone_number,client=client).first()
        if contact_user:
            return JsonResponse({'status':False,'msg':'Error'})

        new_contact_user = ContactUser.objects.create(phone_no=phone_number,country_code_name=country_name,client=client)
        contact_referral.refered_user.add(new_contact_user)
        if contact_referral.is_added == False:
            contact_referral.is_added=True
            # referral_camp = ReferralCampaigns.objects.filter(id=contact_referral.referral_camp.id).first()
            # referral_camp.is_read_count = 1
            # referral_camp.save()
        contact_referral.save()
        
        ref_coupon = Coupon.objects.get(id=contact_referral.referral_camp.ref_coupon.id)

        if ref_coupon.discount_type == "percentage":
            dis_value = digit_roundoff(ref_coupon.discount_value)
            dis_value = f'{dis_value}%'
        else:
            dis_value = digit_roundoff(ref_coupon.discount_value)
            dis_value = f'${dis_value}'

        user_coupon = ContactUserCoupon.objects.create(user=new_contact_user, user_coupon=ref_coupon)
        message = f'{client.business_name}: Woohoo! Here is your {dis_value} OFF voucher: {settings.COUPON_URL}{user_coupon.short_url} This voucher expires in 14 days. See you soon.'
        OneToOneMessage.objects.create(message=message,contact=new_contact_user,client=client,is_send=True)

        try:
            if client.account_sid:
                twi_client = twillio_client(client.account_sid, client.auth_token)
                message_obj = twi_client.messages.create(to=f'{new_contact_user.phone_no}',
                                                     from_=f'{client_phone_no.phone_number}',
                                                     body=message)
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_lineno)

        return JsonResponse({'status':True,'msg':'Done'})


