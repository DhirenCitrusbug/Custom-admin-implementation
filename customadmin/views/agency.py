from django.urls import reverse
from django.views.generic import ListView,UpdateView,DeleteView,CreateView
from aegency_user.models import AgencyUser
from aegency_user.forms import AegencyChangeForm

class AgencyCreateView(CreateView):
    """
    View to create ReviewBrand
    """
    model = AgencyUser
    form_class = AegencyChangeForm
    template_name = "core/agency/agency_create.html"
    permission_required = ("core.add_reviewbrand",)

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("core:agency-list")

class AgencyListView(ListView):
    """
    View for ReviewBrand listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = AgencyUser
    queryset = model.objects.all()
    print(queryset)
    template_name = "core/agency/agency_list.html"
    permission_required = ("core.view_reviewbrand",)


class AgencyUpdateView(UpdateView):
    """
    View to update ReviewCategory
    """

    model = AgencyUser
    form_class = AegencyChangeForm
    template_name = "core/agency/agency_change_form.html"
    permission_required = permission_required = ("core.add_reviewcategory",)

    def get_success_url(self):
        return reverse("core:agency-list")

class AgencyDeleteView(DeleteView):
   model = AgencyUser
   template_name = "core/confirm_delete.html"
   permission_required = permission_required = ("core.add_reviewcategory",)

   def get_success_url(self):
       return reverse("core:agency-list")