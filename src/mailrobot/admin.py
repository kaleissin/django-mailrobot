from django.contrib import admin                                                                                                                  
from django.utils.translation import ugettext_lazy

from .models import Address, Signature, Mail, MailBody

def clone_selected(modeladmin, request, queryset):
    for model in queryset.all():
        model.clone()
clone_selected.short_description =  ugettext_lazy("Clone selected %(verbose_name_plural)s")

class AddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'comment')

class SignatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = [clone_selected]
    prepopulated_fields = {'name': ('sig',)}

class MailAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'sender')
    actions = [clone_selected]

class MailBodyAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    actions = [clone_selected]
    prepopulated_fields = {'name': ('subject',)}

admin.site.register(Address, AddressAdmin)
admin.site.register(Signature, SignatureAdmin)
admin.site.register(Mail, MailAdmin)
admin.site.register(MailBody, MailBodyAdmin)
