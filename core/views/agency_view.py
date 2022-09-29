

from django.shortcuts import reverse
from core.views.generic import (
    MyCreateView,
    MyListView
)


from core.models.agency import AgencyUser,AgencyHostname
from core.forms.agency_forms import AegencyChangeForm

class AgencyUserListView(MyListView):
    """
    View for ReviewCategory listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = AgencyUser
    queryset = model.objects.all()
    template_name = "core/agency_template/ModelYear.html"

class AgencyHostnameListView(MyListView):
    """
    View for ReviewCategory listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = AgencyHostname
    queryset = model.objects.all()
    template_name = "core/agency_template/BikeClass.html"



class AgencyCreateView(MyCreateView):
    """
    View to create ReviewCategory
    """
    model = AgencyUser
    form_class = AegencyChangeForm
    template_name = "core/template_change/modelyear_form.html"
    permission_required = ("core.add_reviewcategory",)

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("core:modelyear-list")


# class YearAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
#     """
#     Ajax-Pagination view for ReviewCategory
#     """
#     model = ModelYear
#     queryset = model.objects.all().order_by("-id")

#     def _get_is_superuser(self, obj):
#         """Get boolean column markup."""
#         t = get_template("core/partials/list_boolean.html")
#         return t.render({"bool_val": obj.is_superuser})

#     def is_orderable(self):
#         """Check if order is defined in dictionary."""
#         # if self._querydict.get("order"):
#         #     return True
#         return True

#     def _get_actions(self, obj):
#         """Get actions column markup."""
#         t = get_template("core/partials/list_row_actions.html")
#         opts = self.model._meta
#         return t.render({
#             "o": obj,
#             "opts": opts,
#             "has_change_permission": self.has_change_permission(self.request),
#             "has_delete_permission": self.has_delete_permission(self.request),
#         })

#     def filter_queryset(self, qs):
#         """Return the list of items for this view."""
#         # If a search term, filter the query
#         if self.search:
#             return qs.filter(
#                 Q(year__icontains=self.search) |
#                 Q(year__icontains=self.search)
#             )
#         return qs

#     def prepare_results(self, qs):
#         """Prepare final result data here."""
#         # Create row data for datatables
#         data = []
#         for o in qs:
#             if o.year:
#                 year = o.year
#             else:
#                 slug = '-'
#             url = reverse("core:reviewcategory-detailview", kwargs={'pk': o.pk})
#             data.append(
#                 {
#                     "id": o.id,
#                     # "name":  "<a href='" + url + "'>" + o.name + "</a>",
#                     "year": o.year,
#                     "actions": self._get_actions(o),
#                 }
#             )
#         return data

#     def get(self, request, *args, **kwargs):
#         context_data = self.get_context_data(request)
#         total_filter_data = len(self.filter_queryset(self.model.objects.all().order_by("-id")))
#         context_data['recordsTotal'] = len(self.model.objects.all().order_by("-id"))
#         context_data['recordsFiltered'] = total_filter_data
#         return JsonResponse(context_data)

# class YearUpdateView(MyUpdateView):
#     """
#     View to update ReviewCategory
#     """

#     model = ModelYear
#     form_class = YearChangeForm
#     template_name = "core/template_change/modelyear_form.html"
#     permission_required = permission_required = ("core.add_reviewcategory",)

#     def get_success_url(self):
#         return reverse("core:modelyear-list")