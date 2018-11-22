from blog.models import post
from django import template
from django.db.models import Count
register=template.Library()
@register.simple_tag
def total_post():
    return post.objects.all().count()
@register.inclusion_tag('blog/blog_post.html')
def latest_post(count):
    Post=post.objects.order_by('-publish')[:count]
    return {'Post':Post}
@register.assignment_tag
def most_comment():
    return post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:3]
