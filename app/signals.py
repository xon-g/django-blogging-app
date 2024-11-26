from app.models import User
from blog.models import Author
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=User, dispatch_uid="update_user_post_save")
def update_user_post_save(sender, instance, **kwargs):
    if hasattr(instance, 'author') and instance.author:
        if instance.author.name != instance.get_full_name():
            instance.author.name = instance.get_full_name()
        if instance.author.email != instance.email:
            instance.author.email = instance.email
        instance.author.save()
    else:
        Author.objects.create(user=instance)