from django.apps import AppConfig


class EtlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'etl'

    def ready(self):
        from etl import signals  # noqa: F401, F403
