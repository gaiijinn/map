from rest_framework.permissions import SAFE_METHODS, BasePermission


class CustomEventsPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.method == 'POST':
            return request.user.is_authenticated

        return request.user.is_authenticated and self._is_creator(request, view)

    def _is_creator(self, request, view):
        """из строки получаем ид, берем обьект если он есть то проверяем что юзер=создатель"""
        if 'pk' in view.kwargs:
            try:
                obj = view.get_object()
                return obj.creator == request.user
            except view.get_queryset().model.DoesNotExist:
                return False
        return False
