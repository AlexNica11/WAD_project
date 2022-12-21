from django.contrib import admin
from .models import HubPageDataModel, ChatMessages, Questions


class ChatMessagesInline(admin.TabularInline):
    model = ChatMessages


class HubPageDataModelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'subject', 'author']}),
        # ('Date information', {'fields': ['date', 'date_end']}),
        ('Starting Date', {'fields': ['date']}),
        ('Ending Date', {'fields': ['date_end']}),
        ('Description', {'fields': ['description']})
    ]
    inlines = [ChatMessagesInline]
    list_display = ('title', 'subject', 'ending_date')
    list_filter = ['subject']
    search_fields = ['title']


admin.site.register(HubPageDataModel, HubPageDataModelAdmin)


class QuestionsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'date', 'user_id', 'contact_id']}),
        ('Message', {'fields': ['message']}),
    ]
    list_display = ('title', )
    list_filter = ['date']
    search_fields = ['title']


admin.site.register(Questions, QuestionsAdmin)

# Register your models here.
