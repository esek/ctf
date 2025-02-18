import os
from typing import Any
from django.db import models

SECRET_LENGTH = 20

class TaskSecretField(models.CharField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs['max_length'] = SECRET_LENGTH
        kwargs['unique'] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self) -> Any:
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        del kwargs['unique']
        return name, path, args, kwargs
    
    def pre_save(self, model_instance: models.Model, add: bool) -> Any:
        value = super().pre_save(model_instance, add)

        if not value:
            value = os.urandom(int(SECRET_LENGTH/2)).hex()   
    
        return value
