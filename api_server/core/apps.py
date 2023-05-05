'''
Module to define the configuration class for the 'core' app
'''
from django.apps import AppConfig

class CoreConfig(AppConfig):
    """
    AppConfig for the core app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
