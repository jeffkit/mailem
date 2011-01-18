#encoding=utf-8

from django.contrib import admin
from mailem.models import MailMessage

class MailMessageAdmin(admin.ModelAdmin):
    list_display = ['subject','priority','create_at']
    search_fields = ['subject','message']

admin.site.register(MailMessage,MailMessageAdmin)
