# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import get_permission_codename
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect

# -----------------------------------------------------------------------------


class SuccessMessageMixin(object):
    """CBV mixin which adds a success message on form save."""

    success_message = ""

    def get_success_message(self):
        return self.success_message

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message()
        if not self.request.is_ajax() and success_message:
            messages.success(self.request, success_message)
        return response

    # def forms_valid(self, forms):
    #     """Ensure it works with multi_form_view.MultiModelFormView."""
    #     print("SuccessMessageMixin:forms_valid")
    #     response = super().forms_valid(forms)
    #     success_message = self.get_success_message()
    #     if not self.request.is_ajax() and success_message:
    #         messages.success(self.request, success_message)
    #     return response


class ModelOptsMixin(object):
    """CBV mixin which adds model options to the context."""

    def get_context_data(self, **kwargs):
        """Returns the context data to use in this view."""
        ctx = super().get_context_data(**kwargs)
        if hasattr(self, "model"):
            ctx["opts"] = self.model._meta
        return ctx


class HasPermissionsMixin(object):
    """CBV mixin which adds has_permission options to the context."""

    def has_add_permission(self, request):

        print('-------------------has_add_permission----------------')
        print('-------------------has_add_permission----------------')
        print('-------------------has_add_permission----------------')


        """
        Return True if the given request has permission to add an object.
        Can be overridden by the user in subclasses.
        """
        opts = self.model._meta
        codename = get_permission_codename("add", opts)
        

        
        return request.user.has_perm("%s.%s" % (opts.app_label, codename)) or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        """
        Return True if the given request has permission to change the given
        Django model instance, the default implementation doesn't examine the
        `obj` parameter.

        Can be overridden by the user in subclasses. In such case it should
        return True if the given request has permission to change the `obj`
        model instance. If `obj` is None, this should return True if the given
        request has permission to change *any* object of the given type.
        """
        opts = self.model._meta
        codename = get_permission_codename("change", opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename)) or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        """
        Return True if the given request has permission to change the given
        Django model instance, the default implementation doesn't examine the
        `obj` parameter.

        Can be overridden by the user in subclasses. In such case it should
        return True if the given request has permission to delete the `obj`
        model instance. If `obj` is None, this should return True if the given
        request has permission to delete *any* object of the given type.
        """
        opts = self.model._meta
        codename = get_permission_codename("delete", opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename)) or request.user.is_staff

    def has_view_permission(self, request, obj=None):
        """
        Return True if the given request has permission to view the given
        Django model instance. The default implementation doesn't examine the
        `obj` parameter.

        If overridden by the user in subclasses, it should return True if the
        given request has permission to view the `obj` model instance. If `obj`
        is None, it should return True if the request has permission to view
        any object of the given type.
        """
        opts = self.model._meta
        codename_view = get_permission_codename("view", opts)
        codename_change = get_permission_codename("change", opts)

        print('----------------------------------', "%s.%s" % (opts.app_label, codename_view),  '----------------------------------' )

        return request.user.has_perm(
            "%s.%s" % (opts.app_label, codename_view)
        ) or request.user.has_perm("%s.%s" % (opts.app_label, codename_change)) or request.user.is_staff

    def has_view_or_change_permission(self, request, obj=None):
        return self.has_view_permission(request, obj) or self.has_change_permission(
            request, obj
        ) or request.user.is_staff

    def has_module_permission(self, request):
        """
        Return True if the given request has any permission in the given
        app label.

        Can be overridden by the user in subclasses. In such case it should
        return True if the given request has permission to view the module on
        the admin index page and access the module's index page. Overriding it
        does not restrict access to the add, change or delete views. Use
        `ModelAdmin.has_(add|change|delete)_permission` for that.
        """
        opts = self.model._meta
        return request.user.has_module_perms(opts.app_label) or request.user.is_staff

    def get_context_data(self, **kwargs):
        """Returns the context data to use in this view."""
        ctx = super().get_context_data(**kwargs)
        if hasattr(self, "model"):
            ctx["has_add_permission"] = self.has_add_permission(self.request)
            ctx["has_change_permission"] = self.has_change_permission(self.request)
            ctx["has_delete_permission"] = self.has_delete_permission(self.request)
            ctx["has_view_permission"] = self.has_view_permission(self.request)
            ctx["has_view_or_change_permission"] = self.has_view_or_change_permission(
                self.request
            )
            ctx["has_module_permission"] = self.has_module_permission(self.request)

            if hasattr(self, "object"):
                ctx["add"] = self.object is None
        return ctx
