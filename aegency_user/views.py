import random
import re
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from admin_user.custom_hostname import custom_hostname_detail
from .models import AgencyUser, Admin, AgencyHostname
# Create your views here.
from django.views import View
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from .forms import AddressChangeForm, AegencyChangeForm, AegencyChangePasswordForm, AegencyWhitelabelDomainForm
from admin_user.models import TimeZone, Country, Address, State
from admin_user.utils import send_templated_email
from client.models import Client
from twilio.rest import Client as twillio_client


class AegencyLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user:
            agency = AgencyUser.objects.filter(id=request.user.id).first()
            if not agency:
                logout(request)
                return redirect('agency-login')
        return super().dispatch(request, *args, **kwargs)


class AgencyUserLoginView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'agency_login.html')
        return redirect('agency-dashboard')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        if not email and not password:
            messages.error(request, 'Please enter E-mail and Password')
            return redirect(request.path)
        if not email:
            messages.error(request, 'Please enter E-mail')
            return redirect(request.path)
        if not password:
            messages.error(request, 'Please enter Password')
            return redirect(request.path)

        user = AgencyUser.objects.filter(email=email).first()
        if user:
            if not user.is_active:
                messages.error(
                    request, 'Your account is currently inactive. Please contact your Administrator')
                return redirect(request.path)
            account = authenticate(email=email, password=password)

            if account:
                login(request, account)
                if not remember:
                    request.session.set_expiry(0)
                return redirect('agency-dashboard')
            else:
                messages.error(
                    request, 'Please enter proper E-mail and Password')
                return redirect(request.path)
        else:
            messages.error(request, 'User does not exists')
            return redirect(request.path)


class AgencyDashboardView(AegencyLoginRequiredMixin, View):
    login_url = 'agency-login'

    def get(self, request):
        time_zone = TimeZone.objects.all().order_by('name')
        country = Country.objects.all().order_by('name')
        business_name = AgencyUser.objects.get(id=request.user.id)
        client = Client.objects.filter(
            aegency=business_name).order_by('business_name')
        return render(request, 'agency_dashboard.html', {'time_zone': time_zone, 'country': country, 'client': client, 'agency': business_name})


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


class ClientDeleteView(View):
    def get(self, request, id):
        print(id)
        client = Client.objects.get(id=id)
        agency=client.aegency
        if client:
            client.delete()
            messages.success(request,'Client deleted successfully')
            return redirect('agency-dashboard')
        return redirect('agency-login')

class AgencyUserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('agency-login')


class AgencySettingView(LoginRequiredMixin, View):
    login_url = 'agency-login'

    def get(self, request):
        aegency = AgencyUser.objects.get(id=request.user.id)
        agency_form = AegencyChangeForm(instance=aegency)
        address = AddressChangeForm(instance=aegency.address)
        client = Client.objects.filter(
            aegency=aegency).order_by('business_name')
        return render(request, 'agency_settings.html', {'add_form': address, 'agency_form': agency_form, 'agency': aegency, 'client': client})

    def post(self, request):
        aegency = AgencyUser.objects.get(id=request.user.id)
        agency_form = AegencyChangeForm(
            request.POST, request.FILES, instance=aegency)
        address = AddressChangeForm(
            request.POST, request.FILES, instance=aegency.address)
        contex = {'add_form': address, 'agency_form': agency_form}
        if address.is_valid():
            address.save()
        if agency_form.is_valid():
            agency_form.instance.address = address.instance
            agency_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(request.path)
        return render(request, 'agency_settings.html', contex)


class AgencyForgetPasswordView(View):
    def get(self, request):
        return render(request, 'agency_forget.html')

    def post(self, request):
        email = request.POST['email']
        # print(email)
        user = AgencyUser.objects.filter(email=email).first()
        # print(user)
        if user:
            user.is_forget = True
            user.save()
            domain = (f'http://{user.whitelabeldomian}' if user.host.is_verified else settings.LOCAL_EMAIL) if user.host and user.whitelabeldomian else settings.LOCAL_EMAIL
            dyanmic_data_for_template = {
                'link': f'{domain}/agency/reset-password/{user.unique_id}',
                'first_name': user.first_name,
                'last_name': user.last_name,
                'subject':settings.AGENCY_FORGOT_PASSWORD

            }
            try:
                send_templated_email(
                    user.email, settings.FORGOT_TEMPLATE, dyanmic_data_for_template)
                messages.success(request, 'E-mail sent successfully')
            except Exception as e:
                print(e)
                messages.error(request, 'E-mail has not been sent')
            return render(request, 'agency_forget.html')
        else:
            messages.error(request, 'User does not exists')
            return render(request, 'agency_forget.html')


class AgencySetPasswordView(View):
    def get(self, request, uuid):
        user = AgencyUser.objects.filter(unique_id=uuid).first()
        if user.is_forget:
            return render(request, 'agency_setpassword.html', {'uuid': uuid})
        else:
            messages.error(request, "Link has been expired")
            return render(request, 'agency_invalid.html')

    def post(self, request, uuid):
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if not password and not confirm_password:
            messages.error(
                request, "Please enter Password and Confirm Password")
            return redirect(request.path)

        user = AgencyUser.objects.filter(unique_id=uuid).first()
        if user:
            user.set_password(password)
            user.is_forget = False
            user.save()
            return redirect('agency-login')
        return render(request, 'agency_invalid.html')


class CountryWiseState(View):
    def get(self, request):
        id = request.GET.get('id', '')
        if id:
            state = State.objects.filter(country__id=id)
            res = [i for i in state.values().order_by('name')]

            response = {
                'status': True,
                'state': res
            }
            return JsonResponse(response)
        state = State.objects.none()
        res = [i for i in state.values().order_by('name')]
        response = {
            'status': True,
            'state': res
        }
        return JsonResponse(response)


class ClientSearch(View):
    def get(self, request):
        term = request.GET.get('term', '')
        order = request.GET.get('order', '')
        business_name = AgencyUser.objects.get(id=request.user.id)
        client = Client.objects.filter(
            aegency=business_name).order_by('-created_at')
        if term:
            client = client.filter(Q(business_name__icontains=term) | Q(
                first_name__icontains=term) | Q(last_name__icontains=term))
        res = [i for i in client.values().order_by('business_name')]
        if order:
            if order.lower() == "up":
                res = [i for i in client.values().order_by('business_name')]
            else:
                res = [i for i in client.values().order_by('-business_name')]
        response = {
            'status': True,
            'client1': res
        }
        return render(request, 'client_list1.html', response)


class CountryView(View):
    def get(self, request):
        country = Country.objects.all().order_by('name')
        return render(request, 'country.html', {'country': country})


class AgencyTwillioView(View):
    def get(self, request):
        aegency = AgencyUser.objects.get(id=request.user.id)
        client = Client.objects.filter(
            aegency=aegency).order_by('business_name')
        return render(request, 'agency_twillio.html', {'agency': aegency, 'client': client})

    def post(self, request):

        acc_sid = request.POST.get('acc_sid', '')
        auth_token = request.POST.get('auth_token', '')
        agency = AgencyUser.objects.get(id=request.user.id)
        client = Client.objects.filter(
            aegency=agency).order_by('business_name')
            
        if AgencyUser.objects.filter(account_sid=acc_sid).exists():
            messages.error(request,"Account SID and Auth Token already exists")
            response = {
                'status': False,
                'message': "Account SID and Auth Token already exists"
            }
            return JsonResponse(response)
        
        if agency.account_sid:
            if not agency.account_sid == acc_sid:
                if acc_sid and auth_token:
                    # print('asdasdas')
                    twil_client = twillio_client(acc_sid, auth_token)

                    try:
                        account_list=twil_client.api.accounts.list(status='active')
                        print(account_list)
                        # message = twil_client.messages.create(
                        #     to="+919016951990",
                        #     from_="+19126122444",
                        #     body="Hello from Python!")
                        for i in client:
                            if not i.account_sid:
                                account = twil_client.api.accounts.create(
                                    friendly_name=i.business_name)
                                i.account_sid = account.sid
                                i.auth_token = account.auth_token
                                i.save()
                                # print(account.__dict__)
                    except Exception as e:
                        print(e)
                        response = {
                            'status': False,
                            'message': "Wrong Account SID and Auth Token"
                        }
                        messages.error(
                            request, 'Wrong Account SID and Auth Token')
                        return JsonResponse(response)

                agency.account_sid = acc_sid
                agency.auth_token = auth_token
                agency.save()
        else:
            if acc_sid and auth_token:
                # print('asdasdas')
                twil_client = twillio_client(acc_sid, auth_token)

                try:
                    account_list=twil_client.api.accounts.list(status='active')
                    print(account_list)
                    # message = twil_client.messages.create(
                    #     to="+919016951990",
                    #     from_="+19126122444",
                    #     body="Hello from Python!")
                    for i in client:
                        if not i.account_sid:
                            account = twil_client.api.accounts.create(
                                friendly_name=i.business_name)
                            i.account_sid = account.sid
                            i.auth_token = account.auth_token
                            i.save()
                            # print(account.__dict__)
                except Exception as e:
                    response = {
                        'status': False,
                        'message': "Wrong Account SID and Auth Token"
                    }
                    messages.error(request, 'Wrong Account SID and Auth Token')
                    return JsonResponse(response)

            agency.account_sid = acc_sid
            agency.auth_token = auth_token
            agency.save()
        response = {
            'status': True,
            'message': "Profile updated susscessfully"
        }
        messages.success(request, 'Profile updated successfully')
        return JsonResponse(response)


def ClientActiveUser(request):
    # Get the product that user has wished for
    user_id = request.POST['user_id']
    active = request.POST['active']
    user = Client.objects.get(id=user_id)
    # print(user)
    domain = (f'http://{user.aegency.whitelabeldomian}' if user.aegency.host.is_verified else settings.LOCAL_EMAIL) if user.aegency.host and user.aegency.whitelabeldomian else settings.LOCAL_EMAIL
    if active == 'True':
        # print('yes')
        user.is_active = True
        user.save()
        dyanmic_data_for_template = {
            'link': f'{domain}',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'agency_name': user.aegency.business_name,
            'subject':settings.CLIENT_ACTIVE_SUBJECT

        }
        try:
            send_templated_email(
                user.email, settings.ACTIVE_USER_TEMPLATE, dyanmic_data_for_template)
        except Exception as e:
            print(e)
            print(e.__traceback__)
            pass
        response = {
            "status": False,
            "id": user_id
        }
        return JsonResponse(response)
    else:
        # print('no')
        user.is_active = False
        user.save()
        dyanmic_data_for_template = {
            'link': f'{domain}',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'agency_name': user.aegency.business_name,
            'subject':settings.CLIENT_INACTIVE_SUBJECT

        }
        try:
            send_templated_email(
                user.email, settings.INACTIVE_USER_TEMPLATE, dyanmic_data_for_template)
        except:
            pass
        response = {
            "status": True,
            "id": user_id
        }
        return JsonResponse(response)


class AgencyChangePasswordView(LoginRequiredMixin, View):
    login_url = 'agency-login'
    
    def get(self, request):
        aegency = AgencyUser.objects.get(id=request.user.id)
        agency_form = AegencyChangePasswordForm(instance=aegency)
        return render(request, 'agency_change_password.html', {'agency_form': agency_form, 'agency': aegency})

    def post(self, request):
        aegency = AgencyUser.objects.get(id=request.user.id)
        agency_form = AegencyChangePasswordForm(request.POST,instance=aegency)
        contex = {'agency_form': agency_form, 'agency': aegency}
        if agency_form.is_valid():
            agency_form.save()
            messages.success(request, 'Password changed successfully')
            return redirect(request.path)
        return render(request, 'agency_change_password.html', contex)


class AgencyWhitelabelSettingView(LoginRequiredMixin, View):
    login_url = 'agency-login'

    def get(self, request):
        aegency = AgencyUser.objects.get(id=request.user.id)
        agency_whitelabel_form = AegencyWhitelabelDomainForm(instance=aegency)
        return render(request, 'agency_whitelabel_domain.html', {'agency_whitelabel_form': agency_whitelabel_form, 'agency': aegency})

    def post(self, request):
        aegency = AgencyUser.objects.get(id=request.user.id)
        agency_whitelabel_form = AegencyWhitelabelDomainForm(request.POST,instance=aegency)
        contex = {'agency_whitelabel_form': agency_whitelabel_form, 'agency': aegency}
        if agency_whitelabel_form.is_valid():
            agency_whitelabel_form.save()
            messages.success(request, 'Whitelabel settings updated successfully')
            return redirect(request.path)
        return render(request, 'agency_whitelabel_domain.html', contex)

class AgencyWhitelabeldomianCheckView(LoginRequiredMixin, View):

    def get(self, request):
        agency = AgencyUser.objects.get(id=request.user.id)
        response=custom_hostname_detail(agency.host.host_id)
        if response['result'].get('ssl'):
            if response['result'].get('ssl').get('status') == "active":
                host=AgencyHostname.objects.filter(id=agency.host.id).first()
                host.is_verified=True
                host.save()

        response['status']=True
        return JsonResponse(response)