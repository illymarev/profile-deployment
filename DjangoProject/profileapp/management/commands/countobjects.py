from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profileapp.models import Profile


class Command(BaseCommand):
    help = 'Prints all models and their counts'

    def count_users(self):
        user = get_user_model()
        users = user.objects.all().count()
        users_info = f'{user} model has {users} objects'
        return users_info

    def count_profiles(self):
        profiles = Profile.objects.all().count()
        profiles_info = f'{Profile} model has {profiles} objects'
        return profiles_info

    def handle(self, *args, **options):
        users = self.count_users()
        profiles = self.count_profiles()
        print(users + '\n' + profiles)
