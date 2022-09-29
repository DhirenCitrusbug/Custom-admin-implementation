
from django.shortcuts import render

# Create your views here.
from django.views.generic import View,TemplateView
from aegency_user.models import AgencyUser
from client.models import Client, ContactUser, ContactUserCoupon



from django.db.models import Sum



# class IndexView(AdminLoginRequiredMixin, View):
#     login_url = '/admin/'

#     def get(self, request):
#         agency = AgencyUser.objects.filter(owner=request.user).order_by('-created_at')[:10]
#         agency_count = list(AgencyUser.objects.filter(owner=request.user).values_list('id'))
#         agency_count = [i[0] for i in agency_count]
#         client_list = list(Client.objects.filter(aegency__id__in=agency_count).values_list('id'))
#         client_list = [i[0] for i in client_list]
#         contact_count = ContactUser.objects.filter(client__id__in=client_list).count()
#         total_sales = ContactUserCoupon.objects.aggregate(Sum('amount'))
#         context = {
#             'agency': agency,
#             'agency_count': len(agency_count),
#             'client_count': len(client_list),
#             'contact_user': contact_count,
#             'total_sales':total_sales,
#         }
#         return render(request, 'admin_dashboard.html', context)

class IndexView(TemplateView):
    template_name = "core/index.html"

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
        return render(request, self.template_name, context)
    

class IndexView(TemplateView):
    template_name = "core/index.html"
    context = {}

    def get(self, request):
        agency_count = list(AgencyUser.objects.filter(owner=request.user).values_list('id'))
        agency_count = [i[0] for i in agency_count]
        self.context['agency'] = AgencyUser.objects.all().count()
        self.context['client'] = len(list(Client.objects.filter(aegency__id__in=agency_count).values_list('id')))
        self.context['contact'] = ContactUser.objects.all().count()
        self.context['total_sales'] = ContactUserCoupon.objects.aggregate(Sum('amount'))
        return render(request, self.template_name, self.context)