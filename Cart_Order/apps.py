from django.apps import AppConfig


class CartOrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Cart_Order'

    def ready(self) -> None:
        import Cart_Order.signals