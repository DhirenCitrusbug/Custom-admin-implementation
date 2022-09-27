
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from ..models import AgencyUser

# Create your views here.
from django.views import View






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