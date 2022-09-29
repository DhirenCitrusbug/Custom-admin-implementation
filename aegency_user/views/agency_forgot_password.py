
from django.conf import settings
from django.contrib import messages
from ..models import AgencyUser
from django.shortcuts import render
# Create your views here.
from django.views import View
from admin_user.utils import send_templated_email
from twilio.rest import Client

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