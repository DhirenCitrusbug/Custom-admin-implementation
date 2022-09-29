from django.shortcuts import render
# Create your views here.
from django.views import View
from admin_user.models import Country





class CountryView(View):
    def get(self, request):
        country = Country.objects.all().order_by('name')
        return render(request, 'country.html', {'country': country})