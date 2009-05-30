from django import template
from tod.comment.forms import CommentForm
register = template.Library()

@register.filter

@register.inclusion_tag("commentarea.html")
def display_comment_area():
    return {"comment_form": CommentForm()}
