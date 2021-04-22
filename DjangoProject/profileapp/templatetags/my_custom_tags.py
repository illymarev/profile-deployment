from django import template
from profileapp.models import Profile
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

register = template.Library()


@register.simple_tag
def edit_list(instance):
    """Use it with profile object to get admin interface change panel, not with user; however, using it with user
    will provide a link to change the user (not his profile)"""
    # return reverse('admin:profileapp_profile_change', args=(instance.id, ))
    if isinstance(instance, Profile):
        return reverse('admin:profileapp_profile_change', args=(instance.id,))
    elif isinstance(instance, get_user_model()):
        return reverse('admin:auth_user_change', args=(instance.id,))
    else:
        return 'Wrong instance'

