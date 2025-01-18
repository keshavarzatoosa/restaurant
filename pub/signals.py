from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Parameters

@receiver(pre_save, sender=Parameters)
def set_type_from_parent(sender, instance, **kwargs):
    if instance.parent is not None:
        instance.type = instance.parent.type