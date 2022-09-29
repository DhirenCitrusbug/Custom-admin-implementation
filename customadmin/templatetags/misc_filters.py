import json

from django import template
from django.conf import settings
from django.contrib.admin.utils import quote
from django.utils.safestring import mark_safe
from django.core.exceptions import ImproperlyConfigured


# -----------------------------------------------------------------------------

register = template.Library()


@register.filter
def model_uname(value):
    """Returns a model name such as 'baking_oils'"""
    words = value._meta.verbose_name.lower().replace("&", "").split()
    return "_".join(words)


@register.filter
def model_name(value):
    # return value.__class__.__name__
    return value._meta.verbose_name.title()


@register.filter
def model_name_plural(value):
    return value._meta.verbose_name_plural.title()


@register.filter(is_safe=True)
def as_json(obj):
    return mark_safe(json.dumps(obj))


# -----------------------------------------------------------------------------
# Misc
# -----------------------------------------------------------------------------


@register.filter
def admin_urlname(value, arg):
    
    # print('---------------------------------------------------------------------------------',value)
    pattern = "%s:%s-%s" % (value.app_label, value.model_name, arg)
    # print('---------------------------------------------------------------------------------',pattern)
    return pattern


@register.filter
def admin_urlquote(value):
    return quote(value)


@register.simple_tag
def field_name(instance, field_name):
    """
    Django template filter which returns the verbose name of an object's,
    model's or related manager's field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()


# @register.simple_tag
# def static_email(path):
#     """
#     Returns an absolute URL to a hosted static image for use in emails.
#     Typically only needed when using local file storage.
#     """
#     if not hasattr(settings, "EMAIL_STATIC_URL"):
#         raise ImproperlyConfigured("The EMAIL_STATIC_URL setting must not be empty.")
#     return f"{settings.EMAIL_STATIC_URL}{path}"


# @register.simple_tag
# def media_email(path):
#     """
#     Returns an absolute URL to a hosted media image for use in emails.
#     Typically only needed when using local file storage.
#     """
#     if not hasattr(settings, "EMAIL_MEDIA_URL"):
#         raise ImproperlyConfigured("The EMAIL_MEDIA_URL setting must not be empty.")
#     return f"{settings.EMAIL_MEDIA_URL}{path}"
