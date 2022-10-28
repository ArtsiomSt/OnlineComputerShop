from django.contrib.auth import mixins
from django.shortcuts import redirect


class AdminUserMixin(mixins.LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_staff:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
