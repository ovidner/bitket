# -*- coding: utf-8 -*-
from guardian.mixins import PermissionRequiredMixin

class MeOrPermissionRequiredMixin(PermissionRequiredMixin):
    """
    Simple mixin checking if the object in `user_attr` is the same as `request.user`. If not, Guardian will check for
    permissions.
    """
    user_attr = None

    def get_user_obj(self):
        if self.user_attr:
            return getattr(self.get_object(), self.user_attr)

        return self.get_object()

    def check_permissions(self, request):
        if not request.user.is_anonymous() and request.user == self.get_user_obj():
            return None
        else:
            return super(MeOrPermissionRequiredMixin, self).check_permissions(request)