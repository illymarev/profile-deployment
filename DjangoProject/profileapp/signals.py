from django.db.models.signals import post_save, post_delete
from django.db import connection
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Notes


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print('Profile created!')
        Notes.objects.create(note=f'{instance} has been created')


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if not created:
        instance.profile.save()
        print('Profile updated!')
        Notes.objects.create(note=f'{instance} has been updated')


@receiver(post_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    Profile.objects.exclude(user=instance)
    print('Profile deleted!')
    Notes.objects.create(note=f'{instance} has been deleted')
