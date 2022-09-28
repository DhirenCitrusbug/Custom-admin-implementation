# -*- coding: utf-8 -*-
"""
This is a view module to define list, create, update, delete views.

You can define different view properties here.
"""

from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin
from django.shortcuts import reverse

from core.mixins import HasPermissionsMixin
from core.views.generic import (
    MyListView, MyDetailView, MyCreateView, MyUpdateView, MyDeleteView, MyLoginRequiredView,
)
from core.forms import ReviewCategoryChangeForm, ReviewCategoryCreationForm
from core.models import ReviewCategory, Review
from django.http import JsonResponse
from django.shortcuts import render
# -----------------------------------------------------------------------------
# ReviewCategory Views
# -----------------------------------------------------------------------------


class ReviewCategoryListView(MyListView):
    """
    View for ReviewCategory listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = ReviewCategory
    queryset = model.objects.all()
    template_name = "core/review_category/review_category_list.html"
    permission_required = ("core.view_reviewcategory",)


class ReviewCategoryDetailView(MyDetailView):

    context = {}

    model = ReviewCategory
    template_name = "core/review_category/review_category_details.html"
    permission_required = ("core.view_reviewcategory",)

    def get_context_data(self, **kwargs):
        """Get context data"""

        context = super().get_context_data(**kwargs)
        context['featured_review'] = Review.objects.filter(id__in=context['reviewcategory'].featured_review.split(','))
        return context

    # def get(self, request, pk):
    #     self.context['review_category_details'] = ReviewCategory.objects.filter(pk=pk).first()
    #     return render(request, self.template_name, self.context)


class ReviewCategoryCreateView(MyCreateView):
    """
    View to create ReviewCategory
    """
    model = ReviewCategory
    form_class = ReviewCategoryCreationForm
    template_name = "core/review_category/review_category_form.html"
    permission_required = ("core.add_reviewcategory",)

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("core:reviewcategory-list")


class ReviewCategoryUpdateView(MyUpdateView):
    """
    View to update ReviewCategory
    """

    model = ReviewCategory
    form_class = ReviewCategoryChangeForm
    template_name = "core/review_category/review_category_form.html"
    permission_required = ("core.change_reviewcategory",)

    def get_success_url(self):
        return reverse("core:reviewcategory-list")


class ReviewCategoryDeleteView(MyDeleteView):
    """
    View to delete ReviewCategory
    """
    model = ReviewCategory
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_reviewcategory",)

    def get_success_url(self):
        return reverse("core:reviewcategory-list")


class ReviewCategoryAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """
    Ajax-Pagination view for ReviewCategory
    """
    model = ReviewCategory
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
                Q(name__icontains=self.search) |
                Q(slug__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        """Prepare final result data here."""
        # Create row data for datatables
        data = []
        for o in qs:
            if o.slug:
                slug = o.slug
            else:
                slug = '-'
            url = reverse("core:reviewcategory-detailview", kwargs={'pk': o.pk})
            data.append(
                {
                    "id": o.id,
                    # "name":  "<a href='" + url + "'>" + o.name + "</a>",
                    "name": o.name,
                    "slug": slug,
                    "reviews": Review.objects.filter(categories=o.id).count(),
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
