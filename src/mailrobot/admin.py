from django.contrib import admin                                                                                                                  

from .models import Address, Signature, Mail, MailBody

class AddressInline(admin.TabularInline):                                   
    model = Address                                                         
    extra = 1

class AddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'comment')

class SignatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'name': ('sig',)}

class MailAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'sender')

class MailBodyAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    prepopulated_fields = {'name': ('subject',)}

admin.site.register(Address, AddressAdmin)
admin.site.register(Signature, SignatureAdmin)
admin.site.register(Mail, MailAdmin)
admin.site.register(MailBody, MailBodyAdmin)
