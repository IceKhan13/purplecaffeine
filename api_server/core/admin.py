"""
Admin module for API server core app
"""

from django.contrib import admin
from .models import Trial

admin.site.register(Trial)
