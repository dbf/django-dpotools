from django.template.defaulttags import register


@register.filter
def breach_get_choice_text(dictionary, key):
    """Used to display the text part of MultiSelectField choices in the
    breach detail view.
    """
    return dictionary.get(key)
