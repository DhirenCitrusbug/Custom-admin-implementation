from frontend.shortcodes import parser
from django import template
from math import floor, ceil

register = template.Library()


def shortcodes_replace(value, request=None):
    """
    A filter for parsing a string on the format ``[shortcode keyword=value]``
    using the shortcodes parser method.
    """
    return parser.parse(value, request)

@register.simple_tag
def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()

def float_to_value(x):
	if x > 10**6-1:
		return str(x/10**6) + 'M'
	elif x > 10**3-1:	
		return str(x/10**3) + 'K'
	else:
		return str(x)


def category_name_clean(name):
	name = name.replace('-', ' ')
	return name.title()


def search_tags_name(name):
	name = name.replace('_', ' ')
	return name.title()


register.filter('shortcodes', shortcodes_replace)
register.filter('float_to_value', float_to_value)
register.filter('category_name_clean', category_name_clean)
register.filter('search_tags_name', search_tags_name)
