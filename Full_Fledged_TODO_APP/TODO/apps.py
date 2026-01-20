from django.apps import AppConfig


class TodoConfig(AppConfig):
    name = 'TODO'


    def ready(self):
        import TODO.signals