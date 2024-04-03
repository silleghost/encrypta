from rest_framework import permissions

class TotpPermission(permissions.BasePermission):
    message = "Вы должны сначала осуществить вход"

    def has_permission(self, request, view):
        return request.session.get('totp_login', False)