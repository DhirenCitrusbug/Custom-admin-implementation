from datetime import date


def parse(attrs, tag_contents=None):
    year = date.today().year
    return str(year)
