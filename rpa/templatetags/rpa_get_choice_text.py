from django.template.defaulttags import register


@register.filter
def rpa_get_choice_text(dictionary, key):
    """Used to display the descriptive text part of MultiSelectField
    choices in the RPA detail view.
    """
    return dictionary.get(key)
