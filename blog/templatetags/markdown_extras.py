from django import template
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def md(value):
    return mark_safe(
        markdown.markdown(
            value,
            extensions=[
                'extra',
                'codehilite'
            ]
        )
    )