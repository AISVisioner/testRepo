from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(User, UserAdmin)