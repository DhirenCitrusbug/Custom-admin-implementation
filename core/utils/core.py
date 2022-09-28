import json
import os
import uuid

from django.contrib.admin.utils import NestedObjects
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.text import capfirst
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from core.models import User
# -----------------------------------------------------------------------------


def update_order(order_data, model):
    """Parse json data and update model order.
    Object keys should be: id, order"""
    jsondata = json.loads(order_data)
    for s in jsondata:
        # This may occur if we have an empty placeholder, it's ok
        if "id" not in s or s["id"] == "None":
            continue
        try:
            instance = model.objects.get(pk=s["id"])
            if instance.the_order != s["order"]:
                instance.the_order = s["order"]
                instance.save()
        except model.DoesNotExist:
            # Object may have been deleted, so just keep going
            continue


def get_upload_to_uuid(self, filename):
    """Rename uploaded file to a unique name."""
    basename = os.path.basename(filename)
    ext = os.path.splitext(basename)[1].lower()
    new_name = uuid.uuid4().hex
    return os.path.join(self.upload_to, new_name + ext)


def get_deleted_objects(objs):
    """Based on `django/contrib/admin/utils.py`"""
    collector = NestedObjects(using="default")
    collector.collect(objs)

    def format_callback(obj):
        opts = obj._meta
        # Display a link to the admin page.
        try:
            return format_html(
                '{}: <a href="{}">{}</a>',
                capfirst(opts.verbose_name),
                # TODO: Is this going to be stable if we use something other than PK, no
                reverse(admin_urlname(opts, "update"), kwargs={"pk": obj.pk}),
                obj,
            )
        except NoReverseMatch:
            pass

        no_edit_link = "%s: %s" % (capfirst(opts.verbose_name), force_text(obj))
        return no_edit_link

    to_delete = collector.nested(format_callback)
    protected = [format_callback(obj) for obj in collector.protected]
    model_count = {
        model._meta.verbose_name_plural: len(objs)
        for model, objs in collector.model_objs.items()
    }

    return to_delete, model_count, protected


def admin_urlname(value, arg):
    """Given model opts (model._meta) and a url name, return a named pattern.
    URLs should be named as: core:app_label:model_name-list"""

    if value.model_name == 'groupinvitation':
        pattern = "%s:%s-%s" % (value.app_label, 'groups', arg)

    elif value.model_name == 'eventinvitation' :
        pattern = "%s:%s-%s" % (value.app_label, 'event', arg)
    else:
        pattern = "%s:%s-%s" % (value.app_label, value.model_name, arg)

    return pattern


def filter_perms():
    """Remove permissions we don't need to worry about managing."""
    return Permission.objects.exclude(
        content_type_id__app_label__in=settings.ADMIN_HIDE_PERMS
    )


def filter_superadmin():
    return User.objects.exclude(
        is_superuser=True
        )


def filter_admin():
    return User.objects.exclude(
        is_staff=True
        )


def filter_vendor():
    vendor = Group.objects.get(name="Vendor")
    return User.objects.filter(
        groups=vendor
    )
