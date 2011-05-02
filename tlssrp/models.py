from tlslite import mathtls
from base64 import b64encode

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

class SRPUserInfo(models.Model):
    user = models.OneToOneField(User)
    srp_group = models.IntegerField(choices=((1024,1024), (1536,1536), (2048,2048)), blank=True)
    verifier = models.TextField(max_length=1000, blank=True)
    salt = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255, blank=True, null=True,
                                help_text='Sets SRP verifier and salt')

    def set_verifier_from_password(self, password):
        N, g, s, v = mathtls.makeVerifier(self.user.username,
                                          password,
                                          self.srp_group)
        self.srpN = b64encode(mathtls.numberToString(N))
        self.srpg = str(g)
        self.verifier = b64encode(mathtls.numberToString(v))
        self.salt = b64encode(s)


@receiver(pre_save, sender=SRPUserInfo)
def set_verifier_from_password(sender, **kwargs):
    srpinfo = kwargs['instance']
    if srpinfo.password:
        srpinfo.set_verifier_from_password(srpinfo.password)
        srpinfo.password = None
