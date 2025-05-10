from django.apps import AppConfig


class AgricultureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'agriculture'
class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        import myapp.signals