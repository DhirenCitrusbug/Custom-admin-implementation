
from django.shortcuts import render
from ..views.aegency_login_required_mixin import AegencyLoginRequiredMixin
# Create your views here.
from django.views import View
from admin_user.models import TimeZone, Country
from ..models import AgencyUser


from client.models import Client

class AgencyDashboardView(AegencyLoginRequiredMixin, View):
    login_url = 'agency-login'

    def get(self, request):
        time_zone = TimeZone.objects.all().order_by('name')
        country = Country.objects.all().order_by('name')
        business_name = AgencyUser.objects.get(id=request.user.id)
        client = Client.objects.filter(
            aegency=business_name).order_by('business_name')
        return render(request, 'agency_dashboard.html', {'time_zone': time_zone, 'country': country, 'client': client, 'agency': business_name})