from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'members'

    def ready(self):
        import members.signals