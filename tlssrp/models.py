from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from .tpasswd import TPasswdFile

class SRPUserInfo(models.Model):
    user = models.OneToOneField(User)
    verifier = models.TextField(max_length=1000, blank=False)
    salt = models.CharField(max_length=255, blank=False)
    group_index = models.IntegerField(default=1)

#User.get_srp_userinfo = get_srp_userinfo

from django.db.models.signals import post_save
from django.dispatch import receiver
#from django.contrib.auth.models import User

@receiver(post_save, sender=SRPUserInfo)
def add_to_srp_passwd(sender, **kwargs):
     srpinfo = kwargs['instance']
     user = srpinfo.user
     passwdfile = TPasswdFile(settings.SRP_PASSWD_FILE)
     passwdfile.put(user.username, srpinfo.verifier,
                    srpinfo.salt, srpinfo.group_index)
