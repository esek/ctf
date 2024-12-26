from django.apps import AppConfig


class BrowserDevtoolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "browser_devtools"
    has_tasks = True
    display_name = "Browser Devtools"
