from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserIsAuthenticated(BasePermission):
    """
    Allows access to authenticated users exclusively.

    Example::

        class MyView(GenericAPIView):
            permission_classes = [UserIsAuthenticated]

    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_authenticated_user)


class NodeIsAuthenticated(BasePermission):
    """
    Allows access to authenticated nodes exclusively.

    Example::

        class MyView(GenericAPIView):
            permission_classes = [NodeIsAuthenticated]

    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_authenticated_node)


class UserIsAuthenticatedOrReadOnly(BasePermission):
    """
    Allows access to authenticated users exclusively, or is a read-only request.

    Example::

        class MyView(GenericAPIView):
            permission_classes = [UserIsAuthenticatedOrReadOnly]

    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.is_authenticated_user
        )


class IsNodeAuthenticatedOrReadOnly(BasePermission):
    """
    Allows access to authenticated nodes exclusively, or is a read-only request.

    Example::

        class MyView(GenericAPIView):
            permission_classes = [IsNodeAuthenticatedOrReadOnly]

    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.is_authenticated_node
        )
