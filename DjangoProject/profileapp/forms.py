from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('edit_ip', 'user')
        widgets = {
            'date_of_birth': AdminDateWidget()
        }

