from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class EventTimeResource(resources.ModelResource):
    class Meta:
        model = EventTime


class EventAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    # search_fields = ['owner']
    list_display = ('owner','event','start_datetime','end_datetime', 'time_excess', 'time_afk', 'is_skipped')
    # form = EventTimeForm
    # add_form = UserCreationForm
    # list_display = ('id','first_name','last_name','email', 'is_staff', 'is_active', 'is_superuser', )
    # list_filter = ('email', 'is_staff', 'is_active',)
    # ordering = ('-id',)
    resource_class = EventTimeResource

# Register your models here.
admin.site.register(Event)
admin.site.register(EventTime,EventAdmin)




