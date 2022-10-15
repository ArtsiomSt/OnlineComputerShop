from django.contrib import admin
from .models import Videocard, Proccessor, Memory, Computer, Manufact, Provider, Category


admin.site.register(Manufact)
admin.site.register(Provider)
admin.site.register(Proccessor)
admin.site.register(Videocard)
admin.site.register(Category)
admin.site.register(Memory)
# Register your models here.
