from django.db.models.signals import post_save
from django.contrib.auth.models import User # sender (User) is the model that sends the signal
from django.dispatch import receiver # receiver is the function that gets the signal and performs some task
from .models import Profile

@receiver(post_save, sender=User) # when a user is saved, send this signal (post_save) and the receiver (create_profile) will receive it
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) # instance is the user that was created

@receiver(post_save, sender=User) # when a user is saved, send this signal (post_save) and the receiver (save_profile) will receive it
def save_profile(sender, instance, **kwargs):
    instance.profile.save()