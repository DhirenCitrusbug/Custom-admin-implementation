from django.contrib.auth import logout
from django.views import View
from django.shortcuts import redirect


class AgencyUserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('agency-login')
