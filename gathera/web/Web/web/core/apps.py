from django.apps import AppConfig


class ProgressConfig(AppConfig):
    name = 'web.core'
    verbose_name = "Users Sessions"

    def ready(self) -> None:
        import web.core.signals

