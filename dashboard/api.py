from dashboard.models import Measure, Node
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
import datetime
from django.db.models import Max


class ReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['get', 'GET']:
            return True
