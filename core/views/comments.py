# -*- coding: utf-8 -*-
"""
This is a view module to define list, create, update, delete views.

You can define different view properties here.
"""
import datetime

from django.db.models import Q, F
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin
from django.shortcuts import reverse, redirect

from core.mixins import HasPermissionsMixin
from core.views.generic import (
    MyListView, MyDetailView, MyCreateView, MyUpdateView, MyDeleteView, MyLoginRequiredView, MyNewFormsetCreateView
)
from core.forms import CommentsCreationForm, CommentsChangeForm
from core.models import (
    Comments, Review, ReviewBrand, ReviewCategory, Pages
)
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from core.utils import send_reply_mail
# -----------------------------------------------------------------------------
# Comments Views
# -----------------------------------------------------------------------------


class CommentsListView(MyListView):
    """
    View for Comments listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = Comments
    queryset = model.objects.all()
    template_name = "core/comment/comment_list.html"
    permission_required = ("core.view_comments",)


class CommentsCreateView(MyCreateView):
    """
    View to create Comments
    """
    model = Comments
    form_class = CommentsCreationForm
    template_name = "core/comment/comment_form.html"
    permission_required = ("core.add_comment",)

    def form_valid(self, form):
        qry_comment = Comments.objects.filter(id=self.request.POST['parent_id'])
        if qry_comment.exists:
            form.instance.name = self.request.user.full_name
            form.instance.email = self.request.user.email
            form.instance.is_approved = True
            form.instance.parent_id = qry_comment[0]
            form.instance.comment_type = qry_comment[0].comment_type
            form.instance.comment_type_id = qry_comment[0].comment_type_id
            qry_comment.update(is_approved=True)
        else:
            form.instance.parent_id = None
        return super().form_valid(form)

    def get_success_message(self):
        return "Record created successfully."

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("core:comments-list")


class CommentsUpdateView(MyUpdateView):
    """
    View to update Comments
    """

    model = Comments
    form_class = CommentsChangeForm
    template_name = "core/comment/comment_form.html"
    permission_required = ("core.change_comments",)

    def get_success_message(self):
        return "Record updated successfully."

    def get_success_url(self):
        return reverse("core:comments-list")


class CommentsDeleteView(MyDeleteView):
    """
    View to delete Comments
    """
    model = Comments
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_comments",)

    def get_success_message(self):
        return "Record deleted successfully."

    def get_success_url(self):
        return reverse("core:comments-list")


class CommentsAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """
    Ajax-Pagination view for Comments
    """
    model = Comments
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
        t = get_template("core/partials/comments_row_actions.html")
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
        comment_data = self.request.GET.get('comment_data')
        if comment_data == 'all':
            if self.search:
                return qs.filter(~Q(is_spam=True),
                    Q(name__icontains=self.search) | Q(email__icontains=self.search) | Q(
                        description__icontains=self.search)
                )
            else:
                return qs.filter(~Q(is_spam=True))
        elif comment_data == 'approved':
            if self.search:
                return qs.filter(~Q(is_spam=True),
                                 Q(name__icontains=self.search) | Q(email__icontains=self.search) | Q(description__icontains=self.search), is_approved=True
                                 )
            else:
                return qs.filter(~Q(is_spam=True), is_approved=True)
        elif comment_data == 'disapproved':
            if self.search:
                return qs.filter(~Q(is_spam=True),
                                 Q(name__icontains=self.search) | Q(email__icontains=self.search) | Q(
                                     description__icontains=self.search), is_approved=False
                                 )
            else:
                return qs.filter(~Q(is_spam=True), is_approved=False)
        elif comment_data == 'spam':
            if self.search:
                return qs.filter(Q(name__icontains=self.search) | Q(email__icontains=self.search) | Q(
                                     description__icontains=self.search), is_spam=True
                                 )
            else:
                return qs.filter(is_spam=True)
        else:
            if self.search:
                return qs.filter(Q(name__icontains=self.search) | Q(email__icontains=self.search) | Q(
                    description__icontains=self.search))
            else:
                return qs

    def response_to(self, obj):
        context_type = obj.comment_type
        comment_type_id = obj.comment_type_id
        name = None
        if context_type == 'Review':
            name = Review.objects.filter(id=comment_type_id).values('name')
        elif context_type == 'Brand':
            name = ReviewBrand.objects.filter(id=comment_type_id).values('name')
        elif context_type == 'Category':
            name = ReviewCategory.objects.filter(id=comment_type_id).values('name')
        elif context_type == 'Custom_Landing':
            name = Pages.objects.filter(id=comment_type_id).value(F(name='page_title'))
        if name.exists():
            return name[0]['name']
        else:
            return None


    def prepare_results(self, qs):
        """Prepare final result data here."""
        # Create row data for datatables
        comment_data = self.request.GET.get('comment_data')
        # qs.filter(is_approved=True)
        data = []
        for o in qs:
            if o.email:
                email = o.email
            else:
                email = '-'

            if o.name:
                name = o.name
            else:
                name = 'Anonymous'

            if o.parent_id:
                description = '<p>In reply to <b>{}</b>.</p>'.format(o.parent_id.name)+o.description
            else:
                description = o.description

            data.append(
                {
                    "id": o.id,
                    "name": '<strong>'+ name +'</strong><br><a href="mailto:'+ email +'">'+ email +'</a>',
                    "description": description,
                    "in_response_to": self.response_to(o),
                    "create_at": o.create_at.strftime('%d-%m-%Y'),
                    "is_approved": o.is_approved,
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

@csrf_exempt
def approve_disapprove_comment(request):
    if request.method == 'POST':
        comment_id = request.POST['comment_id']
        status = request.POST['status']
        qry_comment = Comments.objects.filter(id=comment_id)
        domain = request.build_absolute_uri('/')[:-1]
        if qry_comment.exists():
            if status == 'false':
                qry_comment.update(is_approved=False)
            else:
                if qry_comment[0].parent_id is not None:
                    if qry_comment[0].parent_id.is_notification:
                        context_type = qry_comment[0].comment_type
                        comment_type_id = qry_comment[0].comment_type_id
                        url = None
                        if context_type == 'Review':
                            qry_review = Review.objects.filter(id=comment_type_id)
                            if qry_review.exists():
                                url = 'http://{}/{}/{}/'.format(domain, qry_review[0].brands.all()[0].slug, qry_review[0].slug)
                        elif context_type == 'Brand':
                            qry_review_brand = ReviewBrand.objects.filter(id=comment_type_id)
                            if qry_review_brand.exists():
                                url = 'http://{}/brand/{}/'.format(domain, qry_review_brand[0].slug)
                        elif context_type == 'Category':
                            qry_review_category = ReviewCategory.objects.filter(id=comment_type_id)
                            if qry_review_category.exists():
                                url = 'http://{}/category/{}/'.format(domain, qry_review_category[0].slug)
                        elif context_type == 'Custom_Landing':
                            qry_page = Pages.objects.filter(id=comment_type_id)
                            if qry_page.exists():
                                url = 'http://{}/{}/'.format(domain, qry_page[0].slug)

                        # Use below function for send comment id.
                        # send_reply_mail(qry_comment[0], url)

                        unsubscribe_url = '{}/customadmin/unsubscribe/{}'.format(domain, qry_comment[0].parent_id.id)
                        send_reply_mail(qry_comment[0], unsubscribe_url)
                qry_comment.update(is_approved=True)
            context = {
                'status': True,
                'message': 'Successfully update comment.'
            }
        else:
            context = {
               'status': False,
               'message': 'This comment is not found.'
            }
    else:
        context = {
           'status': False,
           'message': 'Get method not allowed.'
        }
    return JsonResponse(context)


@csrf_exempt
def spam_unspam_comment(request):
    if request.method == 'POST':
        comment_id = request.POST['comment_id']
        status = request.POST['status']
        qry_comment = Comments.objects.filter(id=comment_id)
        if qry_comment.exists():
            if status == 'false':
                qry_comment.update(is_spam=False)
            else:
                qry_comment.update(is_spam=True)
            context = {
                'status': True,
                'message': 'Successfully update comment.'
            }
        else:
            context = {
               'status': False,
               'message': 'This comment is not found.'
            }
    else:
        context = {
           'status': False,
           'message': 'Get method not allowed.'
        }
    return JsonResponse(context)


def empty_spam_comment(request):
    qry_comment = Comments.objects.filter(is_spam=True)
    qry_comment.delete()
    context = {
        'status': True,
        'message': 'Successfully delete spam comment.'
    }
    return JsonResponse(context)


def unsubscribe_comment(request, pk):
    if pk not in [None, ' ', '']:
        qry_comment = Comments.objects.filter(id=pk)
        if qry_comment.exists():
            qry_comment.update(is_notification=False)
            return HttpResponse('Successfully unsubscribe comment replay.')
        else:
            return HttpResponse('Please enter valid URl.')
    else:
        return HttpResponse('Please enter valid URl.')