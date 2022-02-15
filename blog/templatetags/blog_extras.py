from django.contrib.auth import get_user_model

# Before the filter can be used, it needs to be registered 
# into the template library

from django import template

from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from blog.models import Post

import logging


logger = logging.getLogger(__name__)

user_model = get_user_model()

register = template.Library()

@register.filter
def author_details(author, current_user=None):
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ""
    
    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = escape(f"{author.first_name} {author.last_name}")
    else:
        name = escape(f"{author.username}")

    if author.email:
        # email = escape(author.email)
        # prefix = f'<a href="mailto:{email}">'
        # Otra forma de hacerlo
        prefix = format_html('<a href="mailto:{}">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    #return mark_safe(f"{prefix}{name}{suffix}")
    return format_html('{}{}{}', prefix, name, suffix)

@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
    return format_html("</div>") 


@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    logger.debug("Loaded %d recent posts for post %d", len(posts), post.pk)    
    return {"title": "Recent Posts", "posts": posts}

@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)

@register.simple_tag
def endcol():
    return format_html("</div>")    