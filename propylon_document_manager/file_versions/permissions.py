from typing import Any
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsFileOwner(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        if hasattr(obj, "file"):
            return obj.file.user == request.user
        return obj.user == request.user
