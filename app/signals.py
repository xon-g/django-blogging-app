from app.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=User, dispatch_uid="update_user_post_save")
def update_user_post_save(sender, instance, **kwargs):
    if instance.author:
        if instance.author.name != instance.get_full_name():
            instance.author.name = instance.get_full_name()
        if instance.author.email != instance.email:
            instance.author.email = instance.email
        instance.author.save()