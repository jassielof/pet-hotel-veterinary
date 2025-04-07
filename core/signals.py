from django.db.models import signals
from core.models import HistorialPeso
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.dispatch import receiver


@receiver(signals.post_save, sender=HistorialPeso)
def keep_latest_records(sender, instance, **kwargs):
    # Call the discard_old_records function after a new record is saved
    discard_old_records(sender, instance, **kwargs)


def discard_old_records(sender, instance, **kwargs):
    max_records = 10
    records_to_keep = HistorialPeso.objects.filter(
        codigo_mascota=instance.codigo_mascota
    ).order_by("-fecha_registro")[:max_records]

    # Delete records beyond the maximum allowed
    HistorialPeso.objects.filter(codigo_mascota=instance.codigo_mascota).exclude(
        fecha_registro__in=[record.fecha_registro for record in records_to_keep]
    ).delete()
