from django.db.models.signals import post_save
from django.dispatch import receiver

from etl_panel.enums import ProcessStatus
from etl_panel.models import Process


@receiver(post_save, sender=Process)
def create_or_update_periodic_task(
    sender: Process,
    instance: Process,
    created: bool,
    **kwargs,
):
    """Функция-триггер для отправки задачи в Celery при создании процесса передачи данных."""
    if created:
        instance.setup_task()
    else:
        if instance.task is not None:
            instance.task.enabled = instance.status == ProcessStatus.ACTIVE
            instance.task.save()
