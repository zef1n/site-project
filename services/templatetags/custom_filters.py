import re
from django import template
import html  # Модуль для обработки HTML-сущностей

register = template.Library()


@register.filter
def strip_html(value):
    """
    Удаляет все HTML-теги и преобразует HTML-сущности в обычные символы.
    """
    # Убираем HTML-теги
    clean = re.compile('<.*?>')
    clean_text = re.sub(clean, '', value)

    # Преобразуем HTML-сущности (&nbsp;, &mdash; и т.д.) в обычные символы
    clean_text = html.unescape(clean_text)

    return clean_text
