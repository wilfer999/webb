from django.apps import AppConfig


class ViewBasicConfig(AppConfig):
    name = 'view_basic'
    verbose_name = "Restaurant"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
