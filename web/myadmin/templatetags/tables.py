from django import template
from myadmin import models
register = template.Library()

# 自定义标签
from django.utils.html import format_html
@register.simple_tag
def nbsp(a):
    res = a.count(',')-1
    res1 = res*'|----'
    return format_html(res1)
# 计算
from django.utils.html import format_html
@register.simple_tag
def pricexj(num,price):
    res = num*price
    return res

from django.utils.html import format_html
@register.simple_tag
def count(a):
    user = models.Users.objects.get(phone=a)
    counts = models.Cart.objects.filter(uid=user)
    return len(counts)