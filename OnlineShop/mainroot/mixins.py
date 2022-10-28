from django.contrib.auth import mixins
from django.shortcuts import redirect


class AdminUserMixin(mixins.LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_staff:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class GetFieldsForPageMixin():
    def get_field_for_page(self):
        allowed_fields = {
            'title': 'Title',
            'freq': 'Frequency',
            'socket': 'Socket',
            'c_memory': 'Cash memory',
            'weight': 'Weight',
            'memory_type': 'Memory type',
            'remain_stock': 'In stock',
            'v_memory': 'Video memory',
        }
        fields_for_iter =self.__dict__
        fields_for_stats = {}
        for key, value in fields_for_iter.items():
            if key not in allowed_fields.keys():
                continue
            else:
                fields_for_stats[allowed_fields[key]] = fields_for_iter[key]
        return fields_for_stats
