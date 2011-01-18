#encoding=utf-8

from django.contrib import admin
from mailem.models import MailMessage

class MailMessageAdmin(admin.ModelAdmin):
    list_display = ['subject','priority','create_at']
    search_fields = ['subject','message']
    fieldsets =  (
        ('',{
            'fields':('subject','recipients','message','from_email','priority')
        }),
    )

    def queryset(self,request):
        qs = super(MailMessageAdmin,self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self,request,obj,form,change):
        if getattr(obj,'user',None) is None:
            obj.user = request.user
        obj.save()

admin.site.register(MailMessage,MailMessageAdmin)
