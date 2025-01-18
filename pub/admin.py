from django.contrib import admin
from .models import Parameters


class ParametersAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'parent', 'type')

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.parent is not None:
            return ['type']
        return []

admin.site.register(Parameters, ParametersAdmin)
