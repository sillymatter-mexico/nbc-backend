from django.contrib import admin
from users.models import ClientUser, Session, StaffUser

# Register your models here.

@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'uuid']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'uuid']


@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'uuid']
