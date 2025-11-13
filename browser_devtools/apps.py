from django.apps import AppConfig


class BrowserDevtoolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "browser_devtools"
    has_tasks = True
    use_docker = True
    container_protocol = "ws"
    display_name = "Browser Devtools"
