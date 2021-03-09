from django.contrib import admin

from web.CAL.models import Stratum


class NoAddNoDeleteAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Stratum, NoAddNoDeleteAdmin)
