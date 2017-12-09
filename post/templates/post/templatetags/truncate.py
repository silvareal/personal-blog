from django import template

register = template.Library()

@register.filter(name="truncate")
def truncate(value, max_length):
    try:
        if len(value) <= max_length:
            return value
        else:
            return value[:max_length] + "..."
    except TypeError:
        return value