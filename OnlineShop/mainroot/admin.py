from django.contrib import admin
from .models import *


class AdminVideocard(admin.ModelAdmin):
    list_display = ('id', 'title', 'remain_in_stock', 'memory_type')


class AdminProccesor(admin.ModelAdmin):
    list_display = ('id', 'title', 'remain_in_stock', 'freq')


class AdminMemory(admin.ModelAdmin):
    list_display = ('id', 'title', 'remain_in_stock', 'mem_type')


class AdminManufactor(admin.ModelAdmin):
    list_display = ('id', 'title', 'country', 'city')


admin.site.register(Manufact, AdminManufactor)
admin.site.register(Provider)
admin.site.register(Proccessor, AdminProccesor)
admin.site.register(Videocard, AdminVideocard)
admin.site.register(Category)
admin.site.register(Memory, AdminMemory)
admin.site.register(Transport)
admin.site.register(Computer)
# Register your models here.
