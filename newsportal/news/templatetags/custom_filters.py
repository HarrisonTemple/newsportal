from django import template

register = template.Library()

BANNED_WORDS = [
    'news', 'what', 'the',
]
CENSOR_STRING = "***"

@register.filter()
def censor(text: str):
    if isinstance(text, str):
        for term in BANNED_WORDS:
            text = text.replace(term, CENSOR_STRING)
    else:
        print(f'censor filter should only be applied to text ({type(text)})')

    return text

@register.simple_tag(takes_context=True)
def with_context(context, **kwargs):
    c = context['request'].GET.copy()
    for key, arg in kwargs.items():
        c[key] = arg
    return c.urlencode()

