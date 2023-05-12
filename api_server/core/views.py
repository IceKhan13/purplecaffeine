"""
Module to handle the views of API calls
"""
from django.db.models import Q
from rest_framework import viewsets
from rest_framework import permissions

from .models import Trial
from .serializers import TrialSerializer


class TrialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Trial model
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrialSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        search_query = query_params.get("query")
        queryset = Trial.objects.all()  # pylint: disable=no-member
        if search_query:
            queryset = Trial.objects.filter(  # pylint: disable=no-member
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )
        return queryset
