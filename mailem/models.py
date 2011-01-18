#encoding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
    MAILER_INSTALLED = True
else:
    from django.core.mail import send_mass_mail
    MAILER_INSTALLED = False

PRIORITIES = (
    ("high", _("high")),
    ("medium",_("medium")),
    ("low", _("low")),
    ("deferred", _("deferred")),
)

class MailMessage(models.Model):
    subject = models.CharField(_('subject'),max_length=200)
    recipients = models.TextField(_('recipients'),help_text=_('separate receipient addresses by comma.'))
    message = models.TextField(_('message'))
    from_email = models.EmailField(_('from_email'),blank=True,null=True)
    priority = models.CharField(max_length=10, choices=PRIORITIES, default="medium")
    create_at = models.DateTimeField(_('create_at'),auto_now_add=True)
    user = models.ForeignKey(User,verbose_name=_('user'),null=True)

    class Meta:
        verbose_name = _('Mail Message')
        verbose_name_plural = _('Mail Messages')

    def __unicode__(self):
        return self.subject

def do_send_email(sender,instance,created,**kwargs):
    if not created:
        return
    # send emails
    if MAILER_INSTALLED:
        # send email by mailer
        for address in instance.recipients.split(','):
            send_mail(instance.subject,instance.message,instance.from_email or None,[address],instance.priority)
        if not getattr(settings,'MAILER_DAEMON_RUNNING',False):
            # if there is not a mailer cron job runnig,invoke the send_all() function to send mails.
            from mailer.engine import send_all
            send_all()
    else:
        # send mail by django
        data = []
        for address in instance.recipients.split(','):
            data.append((instance.subject,instance.message,instance.from_email or None,[address]))
        send_mass_mail(data,True)

post_save.connect(do_send_email,sender=MailMessage,dispatch_uid='send_email_listener')
