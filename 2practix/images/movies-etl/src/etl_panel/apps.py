from django.apps import AppConfig


class EtlPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'etl_panel'

    def ready(self):
        from etl_panel import signals  # noqa: F401, F403
