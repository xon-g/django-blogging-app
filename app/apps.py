from django.apps import AppConfig

class AppConfig(AppConfig):
    name = 'app'
    verbose_name = "App (Core)"

    def ready(self):
        from app import signals