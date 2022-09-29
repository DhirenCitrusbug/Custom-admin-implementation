from django.contrib.auth import logout
from django.shortcuts import redirect
from ..models import AgencyUser
from django.contrib.auth.mixins import  LoginRequiredMixin

class AegencyLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user:
            agency = AgencyUser.objects.filter(id=request.user.id).first()
            if not agency:
                logout(request)
                return redirect('agency-login')
        return super().dispatch(request, *args, **kwargs)
