from django.contrib import admin
from users.models import ClientUser, Session, StaffUser, ReportUsers, UpdateFile
from users.tasks import ReportClientUser, update_file

# Register your models here.

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    raw_id_fields = ['client_user_pk', 'label']
    list_display = ['pk','client_user_pk', 'game' ,'attempt', 'high_score', 'level','uuid']
    search_fields = ['=client_user_pk__club_premier_id']

class SessionInline(admin.TabularInline):
    model = Session
    fields = ['game', 'attempt', 'high_score']

@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ['__str__','created','accumulation', 'uuid']
    inlines = [SessionInline]

@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'uuid']

def Reporte_Usuarios(modeladmin, request, queryset):
    for i in queryset:
        data = {'id': int(i.id)}
        #ReportClientUser.delay(data)
        ReportClientUser(data)

@admin.register(ReportUsers)
class ReportUsers(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'finish_date', 'email', 'url',
                    'percent', 'percent_report')
    fields = ['name', 'email', 'start_date', 'finish_date']
    actions = [Reporte_Usuarios]


def Subir_archivo(modeladmin, request, queryset):
    for i in queryset:
        data = {'id': int(i.id)}
        update_file.delay(data)
        #update_file(data)


@admin.register(UpdateFile)
class UpdateFileAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__']
    fields = ['file']
    actions = [Subir_archivo]