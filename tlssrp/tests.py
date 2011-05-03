import unittest, re, binascii, base64

from django.test import TestCase
from django.contrib.auth.models import User

from safebook.tlssrp.models import SRPUserInfo

class TestSRPUserInfo(TestCase):
    fixtures = ['test.json']

    def test_makes_verifier(self):
        srpinfo = SRPUserInfo(user=User.objects.get(username='jsmith'))
        srpinfo.set_from_password("asdf")
        self.assertTrue(srpinfo.salt)
        self.assertTrue(srpinfo.verifier)
        # print 'Salt:     <%s>' % srpinfo.salt
        # print 'Verifier: <%s>' % srpinfo.verifier
        self.assertTrue(re.match(r'^[a-zA-Z0-9/+=]+$', srpinfo.salt))
        self.assertTrue(re.match(r'^[a-zA-Z0-9/+=]+$', srpinfo.verifier))

class TestRegister(TestCase):
    # Known-good values taken from Appendix B of RFC 5054 (TLS-SRP)
    username = "alice"
    password = "password123"
    raw_salt     = binascii.unhexlify('BEB25379D1A8581EB5A727673A2441EE')
    raw_verifier = binascii.unhexlify('7E273DE8696FFC4F4E337D05B4B375BEB0DDE1569E8FA00A9886D8129BADA1F1822223CA1A605B530E379BA4729FDC59F105B4787E5186F5C671085A1447B52A48CF1970B4FB6F8400BBF4CEBFBB168152E08AB5EA53D15C1AFF87B2B9DA6E04E058AD51CC72BFC9033B564E26480D78E955A5E29E7AB245DB2BE315E2099AFB')
    srp_group = 1024

    salt_b64 = base64.b64encode(raw_salt)
    verifier_b64 = base64.b64encode(raw_verifier)

    def test_register(self):
        postdata = {'username': self.username,
                    'verifier': self.verifier_b64,
                    'salt': self.salt_b64,
                    'srp_group': 1024}
        res = self.client.post('/auth/register', postdata)
        self.assertRedirects(res, 'https://safebook.trustedhttp.org/'+self.username)
        user = User.objects.get(username=self.username)
        srpinfo = SRPUserInfo.objects.get(user=user)
        self.assertEquals(self.salt_b64, srpinfo.salt)
        self.assertEquals(self.verifier_b64, srpinfo.verifier)
        self.assertEquals(self.srp_group, srpinfo.srp_group)
        self.assertEquals(None, srpinfo.password)

class TestAdmin(TestCase):
    fixtures = ['test.json']

    def test_ssl_user_logged_in(self):
        res = self.client.get('/admin/', SSL_SRP_USER='admin')
        self.assertEquals('admin', res.context['user'].username)
        # test has been logged into admin interface:
        self.assertContains(res, 'Models available in the Auth application.')
        self.assertNotContains(res, 'name="this_is_the_login_form"')
