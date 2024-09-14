from markdown import Markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag("main/terminal.html")
def terminal(task, user, program):
    return {"task": task, "user": user, "program": program}


@register.inclusion_tag("main/markdown.html")
def markdown(markup):
    md = Markdown()
    return {"converted": md.convert(markup)}
