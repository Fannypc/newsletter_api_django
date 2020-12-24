from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User
from newsletters.models import Newsletter

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS', 'POST', 'DELETE']


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if obj.owner == request.user:
                return True

        elif request.method in ['PUT', 'PATCH']:
            if obj.owner == request.user:
                return True
            elif obj.guests.all():
                for guest in obj.guests.all():
                    if request.user.id == guest.id:
                        return True
            return False


"""
            if obj.guests.all():
                for guest in obj.guests.all():
                    if obj.owner == request.user or request.user.id == guest.id:
                        bandera = True

                if bandera:
                    return True
                else:
                    return False
            else:
                if obj.owner == request.user:
                    return True
                return False
"""
