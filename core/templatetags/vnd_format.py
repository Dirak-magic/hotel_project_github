from django import template

register = template.Library()

@register.filter
def vnd(value):
    try:
        # Ép về số nguyên và format dấu phẩy, sau đó đổi phẩy thành chấm
        value = int(value)
        return f"{value:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value
