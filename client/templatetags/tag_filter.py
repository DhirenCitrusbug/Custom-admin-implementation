from django import template

register = template.Library()


@register.filter(name='million')
def currency(value):
    if value:
        if float(value) > 1000000:
            div=value/1000000
            return "{}M".format("%.2f" % div)
        elif float(value) < -1000000:
            div=value/1000000
            return "{}M".format("%.2f" % div)
        elif float(value) > 1000:
            div=value/1000
            return "{}K".format("%.2f" % div)
        elif float(value) < -1000:
            div=value/1000
            return "{}K".format("%.2f" % div)
        else:
            return "{}".format("%.2f" % value)
        
            
    return "0"

@register.filter(name='comma')
def comma_fun(value):
    if value:
        div="{:,}M".format(round(value))
        print(value)
        if float(value) > 1000000:
            div=round(value)/1000000
            return "{:,}M".format(round(div))
        if float(value) < -1000000:
            div=round(value)/1000000
            return "{:,}M".format(round(div))
        return div
    return "N/A"


@register.filter(name='twodigit')
def two_digit(value):
    if int(value) < 10:
        number = f"{int(value):02}"
        return number
    return value


@register.filter(name='roundoff')
def digit_roundoff(value):
    float = value - int(value)
    if float:
        return "{}".format("%.2f" % value)
    else:
        return int(value)
    