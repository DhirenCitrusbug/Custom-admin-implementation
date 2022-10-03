
from django.urls import reverse 
from admin_user.forms import EditProfileForm
from admin_user.models import Admin
from .generic import MyUpdateView
from admin_user.forms import EditProfileForm

class UserUpdateView(MyUpdateView):
    """
    View to update User
    """

    model = Admin
    form_class = EditProfileForm
    template_name = "core/adminuser/user_form.html"
    permission_required = ("customadmin.change_user",)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["user"] = self.request.user
    #     return kwargs

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:index")