from client_user.models import Client
from django.urls import reverse
# from client.forms import ClientChangeForm
from ..forms import ClientCreateForm,MyClientChangeForm
from .generic import (
    MyListView,MyLoginRequiredView,MyUpdateView,MyCreateView,MyDeleteView
)
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import get_template
from ..mixins import HasPermissionsMixin
from django_datatables_too.mixins import DataTableMixin
class ClientCreateView(MyCreateView):
    """
    View to create ReviewBrand
    """
    model = Client
    form_class = ClientCreateForm
    template_name = "core/client/client_create.html"
    permission_required = ("client.add_client",)

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:client-list")

class ClientListView(MyListView):
    """
    View for ReviewBrand listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = Client
    queryset = model.objects.all()
    template_name = "core/client/client_list.html"
    permission_required = ("client.view_client",)

# class ClientListView(ListView):
#     """
#     View for ReviewBrand listing
#     """
#     # paginate_by = 25
#     ordering = ["-id"]
#     model = Client
#     queryset = model.objects.all()
#     print(queryset)
#     template_name = "core/client/client_list.html"
#     permission_required = ("core.view_reviewbrand",)

class ClientUpdateView(MyUpdateView):
    """
    View to update ReviewCategory
    """

    model = Client
    form_class = MyClientChangeForm
    template_name = "core/client/client_change_form.html"
    permission_required = permission_required = ("client.add_client",)

    def get_success_url(self):
        return reverse("customadmin:client-list")


class ClientAjaxPagination(DataTableMixin,HasPermissionsMixin, MyLoginRequiredView):
    """
    Ajax-Pagination view for AgencyUser
    """
    model = Client
    queryset = model.objects.all().order_by("-id")

    def _get_is_superuser(self, obj):
        """Get boolean column markup."""
        t = get_template("core/partials/list_boolean.html")
        return t.render({"bool_val": obj.is_superuser})

    def is_orderable(self):
        """Check if order is defined in dictionary."""
        # if self._querydict.get("order"):
        #     return True
        return True

    def _get_actions(self, obj):
        """Get actions column markup."""
        t = get_template("core/partials/list_row_actions.html")
        opts = self.model._meta
        return t.render({
            "o": obj,
            "opts": opts,
            "has_change_permission": self.has_change_permission(self.request),
            "has_delete_permission": self.has_delete_permission(self.request),
        })

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(business_name=self.search) |
                Q(business_email__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        """Prepare final result data here."""
        # Create row data for datatables
        data = []
        for o in qs:
            if o.email:
                slug = o.email
            else:
                slug = '-'

            data.append(
                {
                    "id": o.id,
                    "business_name": o.business_name,
                    "business_email": o.business_email,
                    "agency":o.aegency.business_name,
                    "actions": self._get_actions(o),
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        total_filter_data = len(self.filter_queryset(self.model.objects.all().order_by("-id")))
        context_data['recordsTotal'] = len(self.model.objects.all().order_by("-id"))
        context_data['recordsFiltered'] = total_filter_data
        return JsonResponse(context_data)


class ClientDeleteView(MyDeleteView):
   model = Client
   template_name = "core/confirm_delete.html"
   permission_required = permission_required = ("client.add_client",)

   def get_success_url(self):
       return reverse("customadmin:client-list")