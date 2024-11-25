from blog.models import Author
from django.dispatch import receiver
from django.db.models.signals import pre_save


@receiver([pre_save], sender=Author, dispatch_uid="update_author_pre_save")
def update_author_pre_save(sender, instance, **kwargs):
    if hasattr(instance, 'user') and instance.user:
        if instance.name != instance.user.get_full_name():
            instance.name = instance.user.get_full_name()
        if instance.email != instance.user.email:
            instance.email = instance.user.email
