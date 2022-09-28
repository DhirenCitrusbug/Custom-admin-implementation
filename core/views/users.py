from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views.generic import TemplateView
from core.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyDetailView,
    MyLoginRequiredView,
    MyUpdateView,
)

from core.models import User, ReviewCategory, ReviewBrand, Review
from core.forms import UserChangeForm
from django.contrib.auth.forms import AdminPasswordChangeForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"
    context = {}

    def get(self, request):
        self.context['review_categories'] = ReviewCategory.objects.all().count()
        self.context['review_brands'] = ReviewBrand.objects.all().count()
        self.context['reviews'] = Review.objects.all().count()
        return render(request, self.template_name, self.context)


# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------
class UserUpdateView(MyUpdateView):
    """
    View to update User
    """

    model = User
    form_class = UserChangeForm
    template_name = "core/adminuser/user_form.html"
    permission_required = ("core.change_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("core:index")


class UserPasswordView(MyUpdateView):
    """
    View to change User Password
    """

    model = User
    form_class = AdminPasswordChangeForm
    template_name = "core/adminuser/password_change_form.html"
    permission_required = ("core.change_user",)

    def get_form_kwargs(self):
        """Get data from kwargs"""

        kwargs = super().get_form_kwargs()
        # kwargs['user'] = self.request.user
        kwargs["user"] = kwargs.pop("instance")
        return kwargs
