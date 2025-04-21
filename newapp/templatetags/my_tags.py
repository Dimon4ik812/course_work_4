from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# @register.filter()
# def media_filter(path):
#     if path:
#         return f'/media/{path}'
@register.filter
def media_filter(value):
    if value:
        return mark_safe(value.url)  # Возвращаем только URL из поля ImageField
    return ""  # Возвращаем пустую строку, если значение None


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})
