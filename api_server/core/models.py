"""
Module to initialize the database
"""
import uuid

from django.db import models


class Trial(models.Model):
    """
    Model representing a trial
    """

    uuid = models.CharField(max_length=255, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(default="No description")
    storage = models.JSONField(default=list)
    metrics = models.JSONField(default=list)
    parameters = models.JSONField(default=list)
    circuits = models.JSONField(default=list)
    operators = models.JSONField(default=list)
    artifacts = models.JSONField(default=list)
    texts = models.JSONField(default=list)
    arrays = models.JSONField(default=list)
    tags = models.JSONField(default=list)
    versions = models.JSONField(default=list)
