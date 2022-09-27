from django.shortcuts import redirect
from django.contrib import messages
from ..models import AgencyUser
from django.shortcuts import render
# Create your views here.
from django.views import View


class AgencySetPasswordView(View):
    def get(self, request, uuid):
        user = AgencyUser.objects.filter(unique_id=uuid).first()
        if user.is_forget:
            return render(request, 'agency_setpassword.html', {'uuid': uuid})
        else:
            messages.error(request, "Link has been expired")
            return render(request, 'agency_invalid.html')

    def post(self, request, uuid):
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if not password and not confirm_password:
            messages.error(
                request, "Please enter Password and Confirm Password")
            return redirect(request.path)

        user = AgencyUser.objects.filter(unique_id=uuid).first()
        if user:
            user.set_password(password)
            user.is_forget = False
            user.save()
            return redirect('agency-login')
        return render(request, 'agency_invalid.html')