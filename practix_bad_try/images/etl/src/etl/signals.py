from django.db.models.signals import post_save
from django.dispatch import receiver

from etl.enums import ProcessStatus
from etl.models import Process


@receiver(post_save, sender=Process)
def create_or_update_periodic_task(
    sender: Process,
    instance: Process,
    created: bool,
    **kwargs
):
    """Сигнал для отправки задачи в Celery при создании или редактировании `Process`."""
    if created:
        instance.setup_task()
    else:
        if instance.task is not None:
            instance.task.enabled = instance.status == ProcessStatus.ACTIVE
            instance.task.save()
