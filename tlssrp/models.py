from tlslite import mathtls

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .tpasswd import TPasswdFile

def srpb64encode(s):
    import ctypes as c
    libgnutls = c.CDLL("libgnutls.so")
    class gnutls_datum_t(c.Structure):
        _fields_ = [("data", c.POINTER(c.c_ubyte)),
                    ("size", c.c_uint)]
    libgnutls.gnutls_srp_base64_encode.argtypes = \
        [c.POINTER(gnutls_datum_t),
         c.c_char_p,
         c.POINTER(c.c_uint)]
    bufsize = (len(s)*4)/3 + 4 # TODO(sqs): can do 3/4 * len(s), but leave safety margin
    buf = c.create_string_buffer(bufsize)
    datum = gnutls_datum_t(data=c.cast(s, c.POINTER(c.c_ubyte)), size=len(s))
    rv = libgnutls.gnutls_srp_base64_encode(c.pointer(datum), buf,
                                            c.pointer(c.c_uint(bufsize)))
    if rv != 0:
        raise Exception("gnutls_srp_base64_encode returned rv=%d" % rv)
    return buf.value

class SRPUserInfo(models.Model):
    user = models.OneToOneField(User)
    verifier = models.TextField(max_length=1000, blank=True)
    salt = models.CharField(max_length=255, blank=True)
    group_index = models.IntegerField(default=1)
    password = models.CharField(max_length=255, blank=True, null=True,
                                help_text='Sets SRP verifier and salt')

    def get_group_size(self):
        """
        Returns the group size, in bits, of the group at `group_index` in the
        SRP passwd conf file. TODO(sqs): un-hardcode this and actually parse
        the passwd conf file.
        """
        group_sizes = [1024, 1536, 2048]
        return group_sizes[self.group_index-1]
    
    def set_verifier_from_password(self, password):
        N, g, s, v = mathtls.makeVerifier(self.user.username,
                                          password,
                                          self.get_group_size())
        self.salt = srpb64encode(s)
        self.verifier = srpb64encode(mathtls.numberToString(v))


@receiver(pre_save, sender=SRPUserInfo)
def set_verifier_from_password(sender, **kwargs):
    srpinfo = kwargs['instance']
    if srpinfo.password:
        srpinfo.set_verifier_from_password(srpinfo.password)
        srpinfo.password = None
        
@receiver(pre_save, sender=SRPUserInfo)
def add_to_srp_passwd_file(sender, **kwargs):
     srpinfo = kwargs['instance']
     user = srpinfo.user
     passwdfile = TPasswdFile(settings.SRP_PASSWD_FILE)
     passwdfile.put(user.username, srpinfo.verifier,
                    srpinfo.salt, srpinfo.group_index)
