# -*- coding: utf-8 -*-
"""
This is a view module to define list, create, update, delete views.

You can define different view properties here.
"""
import datetime

from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin
from django.shortcuts import reverse, redirect

from core.mixins import HasPermissionsMixin
from core.views.generic import (
    MyListView, MyDetailView, MyCreateView, MyUpdateView, MyDeleteView, MyLoginRequiredView,
)
from core.forms import MenusCreationForm, MenusChangeForm
from core.models import Menus

from django.http import JsonResponse


# -----------------------------------------------------------------------------
# Menus Views
# -----------------------------------------------------------------------------

class MenusListView(MyListView):
    """
    View for Menus listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = Menus
    queryset = model.objects.all()
    template_name = "core/menus/menus_list.html"
    permission_required = ("core.view_menus",)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super(MenusListView, self).get_context_data()
        search_value = self.request.GET.get('s', None)
        if search_value is None:
            qry_parent_menu = Menus.objects.filter(menu_location='main_menu', parent_menu=None).order_by('order').values()
            data = qry_parent_menu
            for parent_menu in data:
                qry_child_menu = Menus.objects.filter(menu_location='main_menu', parent_menu=parent_menu['id']).order_by('order').values()
                parent_menu['child_menu'] = list(qry_child_menu)
            context['menu_list'] = data

        else:
            qry_parent_menu = Menus.objects.filter(menu_location=search_value, parent_menu=None).order_by('order').values()
            data = qry_parent_menu
            for parent_menu in data:
                qry_child_menu = Menus.objects.filter(parent_menu=parent_menu['id']).order_by('order').values()
                parent_menu['child_menu'] = list(qry_child_menu)
            context['menu_list'] = data
        return context


class MenusCreateView(MyCreateView):
    """
    View to create Menus
    """
    model = Menus
    form_class = MenusCreationForm
    template_name = "core/menus/menus_form.html"
    permission_required = ("core.add_menus",)

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("core:menus-list")


class MenusUpdateView(MyUpdateView):
    """
    View to update Menus
    """

    model = Menus
    form_class = MenusChangeForm
    template_name = "core/menus/menus_form.html"
    permission_required = ("core.change_menus",)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("core:menus-list")


class MenusDeleteView(MyDeleteView):
    """
    View to delete Menus
    """
    model = Menus
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_menus",)

    def get_success_url(self):
        return reverse("core:menus-list")


class MenusAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """
    Ajax-Pagination view for Menus
    """
    model = Menus
    queryset = model.objects.all().order_by("-id")

    def _get_is_superuser(self, obj):
        """Get boolean column markup."""
        t = get_template("core/partials/list_boolean.html")
        print("_get_is_superuser", obj.is_superuser)
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
                Q(name__icontains=self.search) | Q(link__icontains=self.search) | Q(menu_location__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        """Prepare final result data here."""
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "name": o.name,
                    "menu_location": o.get_menu_location_display(),
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
