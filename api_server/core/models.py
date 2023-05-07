"""
Module to initialize the database
"""
from django.db import models


class Trial(models.Model):
    """
    Model representing a trial
    """

    name = models.CharField(max_length=255)
    metrics = models.JSONField(default=list)
    parameters = models.JSONField(default=list)
    circuits = models.JSONField(default=list)
    backends = models.JSONField(default=list)
    operators = models.JSONField(default=list)
    artifacts = models.JSONField(default=list)
    texts = models.JSONField(default=list)
    arrays = models.JSONField(default=list)
    tags = models.JSONField(default=list)
