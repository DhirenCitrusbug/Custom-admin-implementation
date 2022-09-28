from django.template import Template, Context
from django.conf import settings
from bs4 import BeautifulSoup
from core.models import Review


def parse(attrs, tag_contents=None):
    tag_atts = {}
    if not 'id' in attrs.keys():
        if 'idval' in attrs.keys() and attrs['idval'][:1] == '=':
            tag_atts['src'] = attrs['idval'][1:]
    else:
        tag_atts['review_id'] = BeautifulSoup(attrs['id'], "html.parser").text.replace("'", "").replace('"', '')
        tag_atts['badge'] = BeautifulSoup(attrs['badge'], "html.parser").text.replace("'", "").replace('"', '')

    html = '<h4>{{ review.name }}</h4>'
    html += '<p>{{ review.description  | truncatechars:100 | safe }}</p>'
    html += '<p>{{ badge }}</p>'

    template = Template(html)
    qry_review = Review.objects.filter(id=int(tag_atts['review_id']))
    if qry_review:
        context = Context({'review': qry_review[0], 'badge': tag_atts['badge']})
        return template.render(context)
    else:
        return 'Review not found'
