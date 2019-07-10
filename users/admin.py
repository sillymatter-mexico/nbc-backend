from django.contrib import admin
from users.models import ClientUser, Session, StaffUser

# Register your models here.

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    raw_id_fields = ['client_user_pk', 'label']
    list_display = ['pk','client_user_pk', 'game' ,'attempt', 'high_score', 'level','uuid']

class SessionInline(admin.TabularInline):
    model = Session
    fields = ['game', 'attempt', 'high_score']

@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'uuid']
    inlines = [SessionInline]

@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'uuid']
