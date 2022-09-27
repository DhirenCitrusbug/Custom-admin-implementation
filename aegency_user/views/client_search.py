from django.db.models import Q
from django.shortcuts import render
from ..models import AgencyUser
# Create your views here.
from django.views import View
from client.models import Client

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