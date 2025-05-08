from django.apps import AppConfig
import os


class BookmngConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookMng'

    def ready(self):
        # Import at ready to avoid AppRegistryNotReady error
        from django.conf import settings

        # Create placeholder image on app startup if it doesn't exist
        placeholder_path = os.path.join(settings.BASE_DIR, 'bookEx', 'static', 'placeholder-book.png')
        if not os.path.exists(placeholder_path):
            # Use relative import to avoid circular import
            from .utils.generate_placeholder import create_simple_placeholder
            create_simple_placeholder()