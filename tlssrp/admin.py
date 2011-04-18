from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from safebook.tlssrp.models import SRPUserInfo

def has_srp_entry(user):
    srpinfo = SRPUserInfo.objects.filter(user=user)
    if srpinfo and srpinfo[0].verifier:
        return True
    else:
        return False
has_srp_entry.short_description = 'TLS-SRP info'
has_srp_entry.boolean = True

class SRPUserInfoInline(admin.StackedInline):
    model = SRPUserInfo        

class UserAdminWithSRPUserInfo(UserAdmin):
    inlines = [SRPUserInfoInline]
    list_display = UserAdmin.list_display + (has_srp_entry,)

admin.site.unregister(User)
admin.site.register(User, UserAdminWithSRPUserInfo)
