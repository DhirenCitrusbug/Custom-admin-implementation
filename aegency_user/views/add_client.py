import random
import string

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from ..models import AgencyUser, Admin
# Create your views here.
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from admin_user.models import TimeZone, Country, Address
from admin_user.utils import send_templated_email
from client.models import Client
from twilio.rest import Client as twillio_client


class AddClientView(View, LoginRequiredMixin):
    def post(self, request):
        # print(request.POST)
        f_name = request.POST.get('first_name', '')
        l_name = request.POST.get('last_name', '')
        b_name = request.POST.get('business_name', '')
        email = request.POST.get('email', '')
        time_zone = request.POST.get('time_zone', '')
        country = request.POST.get('country', '')

        client = Admin.objects.filter(email=email)
        if client:
            response = {
                'status': 'unsuccess',
                'message': 'Email already exists'
            }
            return JsonResponse(response)
        agency = AgencyUser.objects.get(id=request.user.id)
        total_client = Client.objects.filter(aegency=agency).count()
        if total_client >= 50:
            response = {
                'status': 'unsuccess',
                'message': 'You have reached limit to add 50 clients'
            }
            return JsonResponse(response)
        if country:
            country_obj = Country.objects.get(id=country)
            address = Address.objects.create(country=country_obj)

            client = Client.objects.create(first_name=f_name, last_name=l_name, email=email, business_name=b_name,
                                           address=address, aegency=agency)
        else:
            client = Client.objects.create(first_name=f_name, last_name=l_name, email=email, business_name=b_name,
                                           aegency=agency)

        if time_zone:
            time_zone_obj = TimeZone.objects.get(id=time_zone)
            client.time_zone = time_zone_obj
        else:
            if agency.time_zone:
                time_zone_obj = TimeZone.objects.get(id=agency.time_zone.id)
                client.time_zone = time_zone_obj
            else:
                response = {
                    'status': 'unsuccess',
                    'message': 'Please select your time zone otherwise select your agency time zone'
                }
                return JsonResponse(response)

        password = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))
        client.set_password(password)
        client.is_user = True
        client.server_passcode = "12345"
        if agency.account_sid:
            twil_client = twillio_client(agency.account_sid, agency.auth_token)
            account = twil_client.api.accounts.create(
                friendly_name=client.business_name)
            client.account_sid = account.sid
            client.auth_token = account.auth_token
        client.save()

        domain = (f'http://{agency.whitelabeldomian}' if agency.host.is_verified else settings.LOCAL_EMAIL) if agency.host and agency.whitelabeldomian else settings.LOCAL_EMAIL
        dynamic_data_for_template = {
            'first_name': client.first_name,
            'last_name': client.last_name,
            'email': client.email,
            'agency_name': client.aegency.business_name,
            'password': password,
            'subject':settings.WELCOME_CLIENT_SUBJECT,
            'link': f'{domain}',
        }
        try:
            send_templated_email(
                client.email, settings.WELCOME_TEMPLATE, dynamic_data_for_template)
        except:
            pass
        response = {
            'status': 'True',
            'message': 'user created successfull'
        }
        messages.success(request, 'Client created successfully')
        return JsonResponse(response)