from django.apps import AppConfig


class CMemoryHijinks(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "c_memory_hijinks"
    has_tasks = True
    display_name = "C Memory Hijinks"
    use_makefile = True
