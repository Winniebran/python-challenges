from rest_framework import permissions
from rest_framework.views import Request, View
from .models import User


class IsUserEmployee(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User):
        return user == request.user or request.user.is_employee
