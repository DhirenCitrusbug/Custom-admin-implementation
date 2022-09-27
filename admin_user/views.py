import re
import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import View
from admin_user.models import Admin
from aegency_user.models import AgencyUser
from client.models import Client, ContactUser, ContactUserCoupon
from django.contrib.auth.mixins import LoginRequiredMixin

from client.tasks import ClientSendEmailForActivation
from .forms import EditProfileForm, AegencyCreationForm, AgencyEditForm
from .utils import send_templated_email

from django.db.models import Count, Sum
from datetime import date, datetime,timedelta

class AdminLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_admin:
            logout(request)
            return render(request, 'admin_login.html')
        return super().dispatch(request, *args, **kwargs)


class AdminUserLoginView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'admin_login.html')
        if not request.user.is_admin:
            logout(request)
            return render(request, 'admin_login.html')
        return redirect('index')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if not email and not password:
            messages.error(request, 'Please enter E-mail and Password')
            return redirect(request.path)
        if not email:
            messages.error(request, 'Please enter E-mail')
            return redirect(request.path)
        if not password:
            messages.error(request, 'Please enter Password')
            return redirect(request.path)

        if not re.fullmatch(regex, email):
            messages.error(request, 'Invalid Email.')
            return redirect(request.path)

        user = Admin.objects.filter(email=email).first()
        if user:
            if not user.is_admin:
                messages.error(request, 'User does not exists')
                return redirect(request.path)
            account = authenticate(email=email, password=password)

            if account:
                login(request, account)

                return redirect('index')
            else:
                messages.error(request, 'Please enter proper E-mail and Password')
                return redirect(request.path)
        else:
            messages.error(request, 'User does not exists')
            return redirect(request.path)


class IndexView(AdminLoginRequiredMixin, View):
    login_url = '/admin/'

    def get(self, request):
        agency = AgencyUser.objects.filter(owner=request.user).order_by('-created_at')[:10]
        agency_count = list(AgencyUser.objects.filter(owner=request.user).values_list('id'))
        agency_count = [i[0] for i in agency_count]
        client_list = list(Client.objects.filter(aegency__id__in=agency_count).values_list('id'))
        client_list = [i[0] for i in client_list]
        contact_count = ContactUser.objects.filter(client__id__in=client_list).count()
        total_sales = ContactUserCoupon.objects.aggregate(Sum('amount'))
        context = {
            'agency': agency,
            'agency_count': len(agency_count),
            'client_count': len(client_list),
            'contact_user': contact_count,
            'total_sales':total_sales,
        }
        return render(request, 'admin_dashboard.html', context)

class AdminDashboardFilterView(View):
    def get(self,request):
        details = request.GET.get('details','')
        print(details)
        all_agency_count = list(AgencyUser.objects.filter(owner=request.user).values_list('id'))
        all_agency_count = [i[0] for i in all_agency_count]
        all_client_list = list(Client.objects.filter(aegency__id__in=all_agency_count).values_list('id'))
        all_client_list = [i[0] for i in all_client_list]
        if details == 'All':
            agency = AgencyUser.objects.filter(owner=request.user).order_by('-created_at')[:10]
            agency_count = list(AgencyUser.objects.filter(owner=request.user).values_list('id'))
            agency_count = [i[0] for i in agency_count]
            client_list = list(Client.objects.filter(aegency__id__in=agency_count).values_list('id'))
            client_list = [i[0] for i in client_list]
            contact_count = ContactUser.objects.filter(client__id__in=client_list).count()
            total_sales = ContactUserCoupon.objects.aggregate(Sum('amount'))
        
        if details == 'Today':
            today = datetime.utcnow()
            agency = AgencyUser.objects.filter(owner=request.user,created_at__date=today.date()).order_by('-created_at')[:10]
            agency_count = list(AgencyUser.objects.filter(owner=request.user,created_at__date=today.date()).values_list('id'))
            agency_count = [i[0] for i in agency_count]
            client_list = list(Client.objects.filter(aegency__id__in=all_agency_count,created_at__date=today.date()).values_list('id'))
            client_list = [i[0] for i in client_list]
            contact_count = ContactUser.objects.filter(client__id__in=all_client_list,created_at__date=today.date()).count()
            total_sales = ContactUserCoupon.objects.filter(updated_at__date=today.date()).aggregate(Sum('amount'))

        if details == 'Last 7 Days':
            today = datetime.utcnow()
            startdate = datetime.utcnow() - timedelta(days=7)
            agency = AgencyUser.objects.filter(owner=request.user,created_at__range=[startdate,today]).order_by('-created_at')[:10]
            agency_count = list(AgencyUser.objects.filter(owner=request.user,created_at__range=[startdate,today]).values_list('id'))
            agency_count = [i[0] for i in agency_count]
            client_list = list(Client.objects.filter(aegency__id__in=all_agency_count,created_at__range=[startdate,today]).values_list('id'))
            client_list = [i[0] for i in client_list]
            contact_count = ContactUser.objects.filter(client__id__in=all_client_list,created_at__range=[startdate,today]).count()
            total_sales = ContactUserCoupon.objects.filter(updated_at__range=[startdate,today]).aggregate(Sum('amount'))

        if details == 'This Month':
            today = datetime.utcnow()
            startdate = datetime.utcnow() - timedelta(days=today.day)
            agency = AgencyUser.objects.filter(owner=request.user,created_at__range=[startdate,today]).order_by('-created_at')[:10]
            agency_count = list(AgencyUser.objects.filter(owner=request.user,created_at__range=[startdate,today]).values_list('id'))
            agency_count = [i[0] for i in agency_count]
            client_list = list(Client.objects.filter(aegency__id__in=all_agency_count,created_at__range=[startdate,today]).values_list('id'))
            client_list = [i[0] for i in client_list]
            contact_count = ContactUser.objects.filter(client__id__in=all_client_list,created_at__range=[startdate,today]).count()
            total_sales = ContactUserCoupon.objects.filter(updated_at__range=[startdate,today]).aggregate(Sum('amount'))

        context = {
            'agency': agency,
            'agency_count': len(agency_count),
            'client_count': len(client_list),
            'contact_user': contact_count,
            'total_sales':total_sales,
        }

        return render(request, 'admin_dashboard_filter.html', context)

class AdminUserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/admin/')


class AdminEditView(LoginRequiredMixin, View):
    login_url = '/admin/'

    def get(self, request):
        form = EditProfileForm(instance=request.user)
        return render(request, 'admin_settings.html', {'form': form})

    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        context = {"form": form}
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(request.path)
        return render(request, 'admin_settings.html', context=context)


class AdminUserListView(LoginRequiredMixin, View):
    login_url = '/admin/'

    def get(self, request):
        form = AegencyCreationForm()
        admin = Admin.objects.get(id=request.user.id)
        agency = AgencyUser.objects.filter(owner=admin).annotate(client_cam=Count('agency_user'))
        return render(request, 'admin_users.html', {'form': form, 'agency': agency})

    def post(self, request):
        print(request.POST)
        f_name = request.POST.get('first_name', '')
        l_name = request.POST.get('last_name', '')
        b_name = request.POST.get('business_name', '')
        email = request.POST.get('email', '')
        # password=request.POST.get('password','')
        transaction_id = request.POST.get('transaction_id', '')
        plan_duration = request.POST.get('plan_duration', '')

        print(b_name)
        aegency = AgencyUser.objects.filter(email=email)

        if aegency:
            response = {
                'status': 'unsuccess',
                'message': 'Email already exists'
            }
            return JsonResponse(response)

        client = Admin.objects.filter(email=email)

        if client:
            response = {
                'status': 'unsuccess',
                'message': 'Email already exists'
            }
            return JsonResponse(response)

        aegency_user = AgencyUser.objects.create(first_name=f_name, last_name=l_name, email=email, business_name=b_name,
                                                 transaction_id=transaction_id, plan_duration=plan_duration,
                                                 owner=request.user)

        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        aegency_user.set_password(password)
        aegency_user.save()
        domain = (f'http://{aegency_user.whitelabeldomian}' if aegency_user.host.is_verified else settings.LOCAL_EMAIL) if aegency_user.host else settings.LOCAL_EMAIL
        dynamic_data_for_template = {
            'link': f'{domain}/agency/agency-login',
            'first_name': aegency_user.first_name,
            'last_name': aegency_user.last_name,
            'email': aegency_user.email,
            'password': password,
            'subject':settings.WELCOME_AGENCY_SUBJECT
        }
        try:
            send_templated_email(aegency_user.email, settings.AGENCY_WELCOME_TEMPLATE, dynamic_data_for_template)
        except:
            pass
        response = {
            'status': True,
            'message': 'user created successfull'
        }
        messages.success(request, 'Agency created successfully')
        return JsonResponse(response)


def AgencyActiveUser(request):
    # Get the product that user has wished for
    user_id = request.POST['user_id']
    active = request.POST['active']
    user = AgencyUser.objects.get(id=user_id)
    if active == 'True':
        print('yes')
        user.is_active = True
        user.save()
        ClientSendEmailForActivation.delay(user.id, True)
        domain = (f'http://{user.whitelabeldomian}' if user.host.is_verified else settings.LOCAL_EMAIL) if user.host else settings.LOCAL_EMAIL
        dyanmic_data_for_template = {
            'link': f'{domain}/agency/agency-login',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'subject':settings.AGENCY_ACTIVE_SUBJECT
        }
        try:
            send_templated_email(user.email, settings.AGENCY_ACTIVE_USER_TEMPLATE, dyanmic_data_for_template)
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
        print('no')
        user.is_active = False
        user.save()
        ClientSendEmailForActivation.delay(user.id, False)
        domain = (f'http://{user.whitelabeldomian}' if user.host.is_verified else settings.LOCAL_EMAIL) if user.host else settings.LOCAL_EMAIL
        dyanmic_data_for_template = {
            'link': f'{domain}/agency/agency-login',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'subject':settings.AGENCY_INACTIVE_SUBJECT
        }
        try:
            send_templated_email(user.email, settings.AGENCY_INACTIVE_USER_TEMPLATE, dyanmic_data_for_template)
        except Exception as e:
            print(e)
            print(e.__traceback__)
        response = {
            "status": True,
            "id": user_id
        }
        return JsonResponse(response)


class AgencyEditView(LoginRequiredMixin, View):
    login_url = '/admin/'

    def get(self, request):
        agency_id = request.GET.get('agency_id', '')
        agency = AgencyUser.objects.get(id=agency_id)
        res = model_to_dict(agency)

        response = {
            'status': True,
            'message': 'user created successfull',
            'agency': res,
        }
        return JsonResponse(response)

    def post(self, request):
        print(request.POST)
        agency_id = request.POST.get('agency_id', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        business_name = request.POST.get('business_name', '')
        transaction_id = request.POST.get('transaction_id', '')
        plan_duration = request.POST.get('plan_duration', '')
        email = request.POST.get('email','')
 
        if Admin.objects.filter(email=email).exclude(id=agency_id):
            response = {
                    'status': False,
                    'message': 'Email already exists',
                }
            return JsonResponse(response)
        else:
            agency = AgencyUser.objects.get(id=agency_id)
            if not agency:
                response = {
                    'status': False,
                    'message': 'Id is not provide',
                }
                return JsonResponse(response)

            agency.first_name = first_name
            agency.last_name = last_name
            agency.email = email
            agency.business_name = business_name
            agency.transaction_id = transaction_id
            agency.plan_duration = plan_duration
            agency.save()

            response = {
                'status': True,
                'message': 'profile updated successfully',

            }
            messages.success(request, 'Agency updated successfully')
            return JsonResponse(response)          


class AgencyDeleteView(LoginRequiredMixin, View):
    login_url = '/admin/'

    def get(self, request, id):
        agency = AgencyUser.objects.get(id=id)
        if agency:
            agency.delete()
            messages.success(request, 'Agency deleted successfully')
            return redirect('admin-user')
        return render(request, 'admin_users.html')


class StatusWiseFilter(View):

    def get(self, request):
        admin = Admin.objects.get(id=request.user.id)
        agency = AgencyUser.objects.filter(owner=admin).annotate(client_cam=Count('agency_user'))
        status = request.GET.get('status', '')

        if status == "1":
            agency = agency.filter(is_active=True)
            print(agency.count(), "1111111111")

            return render(request, 'agency_table.html', {'agency': agency})
        elif status == "0":
            agency = agency.filter(is_active=False)
            print(agency.count(), "000000000000")
            return render(request, 'agency_table.html', {'agency': agency})
        else:
            print(agency.count(), '22222222222')
            return render(request, 'agency_table.html', {'agency': agency})