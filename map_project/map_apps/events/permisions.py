from rest_framework.permissions import SAFE_METHODS, BasePermission


class CustomEventsPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method == "POST":
            if view.action == "event_report":
                return request.user.is_authenticated

            return request.user.is_authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if view.action in ['event_report']:
            return request.user.is_authenticated

        return obj.creator == request.user
