from django.apps import AppConfig


class BuildsiteBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buildsite_backend'

    def ready(self):
        import buildsite_backend.signals