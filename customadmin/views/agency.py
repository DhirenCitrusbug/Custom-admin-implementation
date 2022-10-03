from multiprocessing.connection import Client
from django.urls import reverse
from aegency_user.models import AgencyUser
from client.models import Client
from ..forms import AgencyCreateForm
from aegency_user.forms import AegencyChangeForm
from .generic import (
    MyListView, MyCreateView, MyUpdateView, MyDeleteView, MyLoginRequiredView,
)
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import get_template
from ..mixins import HasPermissionsMixin
from django_datatables_too.mixins import DataTableMixin

class AgencyCreateView(MyCreateView):
    """
    View to create AgencyUser
    """
    model = AgencyUser
    form_class = AgencyCreateForm
    template_name = "core/agency/agency_create.html"
    permission_required = ("agency_user.add_agencyUser",)

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:agency-list")

class AgencyListView(MyListView):
    """
    View for ReviewBrand listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = AgencyUser
    queryset = model.objects.all()
    template_name = "core/agency/agency_list.html"
    permission_required = ("agency_user.view_agencyuser",)

# class AgencyListView(MyListView):
#     """
#     View for AgencyUser listing
#     """
#     # paginate_by = 25
#     ordering = ["-id"]
#     model = AgencyUser
#     queryset = model.objects.all()
#     print(queryset)
#     template_name = "core/agency/agency_list.html"
#     permission_required = ("core.view_agencyUser",)


class AgencyUpdateView(MyUpdateView):
    """
    View to update ReviewCategory
    """

    model = AgencyUser
    form_class = AegencyChangeForm
    template_name = "core/agency/agency_change_form.html"
    permission_required = ("agency_user.add_agencyuser",)

    def get_success_url(self):
        return reverse("core:agency-list")

class AgencyDeleteView(MyDeleteView):
   model = AgencyUser
   template_name = "core/confirm_delete.html"
   permission_required = permission_required = ("agency_user.add_agencyuser",)

   def get_success_url(self):
       return reverse("customadmin:agency-list")

class AgencyUserAjaxPagination(DataTableMixin,HasPermissionsMixin, MyLoginRequiredView):
    """
    Ajax-Pagination view for AgencyUser
    """
    model = AgencyUser
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
                Q(first_name__icontains=self.search) |
                Q(email__icontains=self.search)
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
                    "first_name": o.first_name,
                    "email": o.email,
                    "clients": Client.objects.filter(aegency=o.id).count(),
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