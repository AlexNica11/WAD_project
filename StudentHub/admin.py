from django.contrib import admin
from .models import HubPageDataModel, ChatMessages


class ChatMessagesInline(admin.TabularInline):
    model = ChatMessages


class HubPageDataModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'subject', 'author']}),
        ('Date information', {'fields': ['date', 'date_end']}),
        ('Description', {'fields': ['description']})
    ]
    inlines = [ChatMessagesInline]
    list_display = ('title', 'subject', 'date_end')
    list_filter = ['date_end']
    search_fields = ['title']


admin.site.register(HubPageDataModel, HubPageDataModelAdmin)
# Register your models here.
