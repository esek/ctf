from markdown import Markdown
from django import template

from ..markdown import CTFExtension

register = template.Library()


@register.inclusion_tag("main/terminal.html")
def terminal(task, user, program):
    return {"task": task, "user": user, "program": program}


@register.inclusion_tag("main/markdown.html")
def markdown(markup):
    md = Markdown(extensions=["codehilite", "fenced_code", CTFExtension()])
    return {"converted": md.convert(markup)}
