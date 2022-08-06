from django.template.defaulttags import register


@register.filter
def get_choice_text(dictionary, key):
    return dictionary.get(key)
