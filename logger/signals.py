from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver



@receiver(post_save,sender = User)
def add_user_to_group(sender, instance, created, **kwargs):
    user = instance
    if created:
        group = Group.objects.get(name='User')
        user.groups.add(group)
        user.is_staff=True
        user.save()
