from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from .models import Profile
from .forms import ProfileForm


# Create your views here.
class ShowProfile(LoginRequiredMixin, DetailView):
    """Detail view function"""
    model = Profile
    login_url = '/accounts/login/'
    template_name = 'show_profile.html'
    redirect_field_name = 'login'


class UpdateProfile(LoginRequiredMixin, UpdateView):
    """Update user function"""
    model = Profile
    template_name = 'update_profile.html'
    form_class = ProfileForm

    def visitor_ip_address(self):
        """Get visitor IP"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_success_url(self):
        """Return to profile in case the update was successful"""
        return reverse('profile:showprofile', kwargs={'pk': self.object.id})

    def get_queryset(self):
        """Allow the user to change only his own profile"""
        qs = super(UpdateProfile, self).get_queryset()
        return qs.filter(user=self.request.user)

    def form_valid(self, form):
        """Function to assign edit_ip"""
        instance = form.save(commit=False)
        # instance.edit_ip = self.request.META['REMOTE_ADDR']
        instance.edit_ip = self.visitor_ip_address()
        instance.save()
        return super().form_valid(form)


def main_page_redirect(request):
    if request.user.is_authenticated:
        response = redirect(reverse('profile:showprofile', args=(request.user.profile.id,)))
        return response
    else:
        response = redirect('/accounts/login/')
        return response
