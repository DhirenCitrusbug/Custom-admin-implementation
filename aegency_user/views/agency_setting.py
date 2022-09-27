from django.contrib import messages
from django.shortcuts import render, redirect
from ..models import AgencyUser
from ..forms import AddressChangeForm, AegencyChangeForm
from client.models import Client
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


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