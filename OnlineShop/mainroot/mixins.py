from django.contrib.auth import mixins
from django.shortcuts import redirect
from django.http.response import HttpResponseForbidden


class AdminUserMixin(mixins.LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_staff:
            return HttpResponseForbidden("Access not granted")
        return super().dispatch(request, *args, **kwargs)


class GetFieldsForPageMixin:
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
            'gabs': "Size",
        }
        connected_fields = {
            "manuf_id": "Manufactor",
            "videocard_id": "Videocard",
            "memory_p_id": "Memory",
            "processor_id": "Processor",
        }
        fields_for_iter =self.__dict__
        fields_for_stats = {}
        for key, value in fields_for_iter.items():
            if key in allowed_fields.keys():
                fields_for_stats[allowed_fields[key]] = fields_for_iter[key]
            if key in connected_fields:
                query = 'self.'+key.replace('_id', '')+'.title'
                print(query)
                fields_for_stats[connected_fields[key]] = eval(query)
        fields_for_stats['Price'] = self.__dict__['price']
        return fields_for_stats
