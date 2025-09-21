"""Stores permission logic for the API."""

import os

from rest_framework.permissions import BasePermission


class HasAPIKey(BasePermission):
    """Check if the API Key is valid."""

    def has_permission(self, request, view):
        """Check if the provided API key matches the valid one."""
        return request.headers.get("X-API-Key") == os.environ["API_KEY"]
