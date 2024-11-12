from django.apps import AppConfig


class VendasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendas'

    def ready(self):
        from . import signals
        import vendas.signals  # Supondo que o app se chama 'vendas'