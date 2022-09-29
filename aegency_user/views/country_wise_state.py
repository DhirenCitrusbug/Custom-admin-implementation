from django.http import JsonResponse
# Create your views here.
from django.views import View
from admin_user.models import State

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