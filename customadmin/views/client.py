from django.views.generic import ListView
from client_user.models import Client
from django.urls import reverse
from django.views.generic import ListView,UpdateView,DeleteView,CreateView
from client.forms import ClientChangeForm

class ClientCreateView(CreateView):
    """
    View to create ReviewBrand
    """
    model = Client
    form_class = ClientChangeForm
    template_name = "core/client/client_create.html"
    permission_required = ("core.add_reviewbrand",)

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("core:client-list")


class ClientListView(ListView):
    """
    View for ReviewBrand listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = Client
    queryset = model.objects.all()
    print(queryset)
    template_name = "core/client/client_list.html"
    permission_required = ("core.view_reviewbrand",)

class ClientUpdateView(UpdateView):
    """
    View to update ReviewCategory
    """

    model = Client
    form_class = ClientChangeForm
    template_name = "core/client/client_change_form.html"
    permission_required = permission_required = ("core.add_reviewcategory",)

    def get_success_url(self):
        return reverse("core:client-list")



class ClientDeleteView(DeleteView):
   model = Client
   template_name = "core/confirm_delete.html"
   permission_required = permission_required = ("core.add_reviewcategory",)

   def get_success_url(self):
       return reverse("core:client-list")