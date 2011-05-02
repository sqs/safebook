import unittest, tempfile, re, binascii, base64

from django.test import TestCase
from django.contrib.auth.models import User

from safebook.tlssrp.models import SRPUserInfo
from .tpasswd import TPasswdFile

SAMPLE_TPASSWD_FILE = "jsmith:7wvgHboUKq0nM1J7wvksijT3/ZKrwg5o5BjMJQgxfXiyQZiimM94yj4DlzQe3upRV68x14i5LA.WjoCXv6TrERVT05f4Keib3BBqjK88.OBTaYheChx71.iq2ckl6PdKO7/.RPoPMtXytOzm5tLQEFQRj4WGnHghYIQ5SwPdPc6:1aZTSV/drqhDRiv8Fd/dI4:1\n\
alice:7TRnEFJUNmJVeGmJ7MeAdClnf1qp54POUyzJF2gFkX6wARm6kPsZSNhwyZ4ZP9iGo5k1WTMxtnkqwDJgdHIodsUo3QjjFA2PnmkB8cODqsj4Cnak5TOx2szgUfb9AUh0Y5wcTIOZ42A6N6HzyEKiGQTB0GSAPdGOVsVspy7TUJG:32eJPdikIgxKJGB84chOEp:1\n\
user:9oaYZehIREyzHN1GR4uxoo3ina6erM8VJR0EfABp/8xjDK4A0Wu69TpV1ylhaV2NKSWVNa4KrUoa4g.KFX2qEOWZPPt49843/hZNC31HQJfPFwwcsqSmLxYrFZvlUqxGn7xlySbhCo/QSDYmo9z1oanN8q6v/DBu3HHevxFBQBv:3QGRPGqxjYrjM9V8wIQVpE:1\n\
carol:1kN4kH3PuUhIbrgP.Kj0BA1ErXyu2ekod3VU9rvESvJxGsrwLK8GiyyDrvgpRN4GgiQsC8gdDq7OkuCUYparyZdreck.4gQUZDuSHbY97sNWksV3eFWPSCD6cLfDhzZC6fDgPVsOCnhdYdMQl1nxtn0lqwWNrDvvGokj0i5XUORCh.qkzCkTQcM/w56gYwh91kAxLuphdFsdafBrpJoZV2rehNKlaecx1xaX7Xc5bW2.dqaZmqVxIRrARMLcE0zKPq4jJgVuTcbKwpae.N6IGxFaFlrgtBAUBZEmljW4EYXQolnlJaphhXkIIl7YkZCBpDavKqIh6DaBXq4dVmRiw2:J.vZf75WgsmWRO35DTdGk:3\n"

class TestTPasswdFile(unittest.TestCase):

    def setUp(self):
        self.tmpfile = tempfile.NamedTemporaryFile()
        self.tmpfile.write(SAMPLE_TPASSWD_FILE)
        self.tmpfile.seek(0)
        self.path = self.tmpfile.name
        self.passwd = TPasswdFile(self.path)

    def tearDown(self):
        self.tmpfile.close()

    def test_get1(self):
        e = self.passwd.get('jsmith')
        self.assertEquals("7wvgHboUKq0nM1J7wvksijT3/ZKrwg5o5BjMJQgxfXiyQZiimM94yj4DlzQe3upRV68x14i5LA.WjoCXv6TrERVT05f4Keib3BBqjK88.OBTaYheChx71.iq2ckl6PdKO7/.RPoPMtXytOzm5tLQEFQRj4WGnHghYIQ5SwPdPc6", e['verifier'])
        self.assertEquals("1aZTSV/drqhDRiv8Fd/dI4", e['salt'])
        self.assertEquals(1, e['group_index'])

    def test_get2(self):
        e = self.passwd.get('carol')
        self.assertEquals("1kN4kH3PuUhIbrgP.Kj0BA1ErXyu2ekod3VU9rvESvJxGsrwLK8GiyyDrvgpRN4GgiQsC8gdDq7OkuCUYparyZdreck.4gQUZDuSHbY97sNWksV3eFWPSCD6cLfDhzZC6fDgPVsOCnhdYdMQl1nxtn0lqwWNrDvvGokj0i5XUORCh.qkzCkTQcM/w56gYwh91kAxLuphdFsdafBrpJoZV2rehNKlaecx1xaX7Xc5bW2.dqaZmqVxIRrARMLcE0zKPq4jJgVuTcbKwpae.N6IGxFaFlrgtBAUBZEmljW4EYXQolnlJaphhXkIIl7YkZCBpDavKqIh6DaBXq4dVmRiw2", e['verifier'])
        self.assertEquals("J.vZf75WgsmWRO35DTdGk", e['salt'])
        self.assertEquals(3, e['group_index'])
        
    def test_get_notfound(self):
        self.assertEquals(None, self.passwd.get('notauser'))

    def test_get_invalid(self):
        self.assertRaises(KeyError, self.passwd.get, '')
        self.assertRaises(KeyError, self.passwd.get, 'some:user')

    def test_put_new(self):
        self.passwd.put('newuser', 'abcdefg12345', 'xyz', 2)
        expected = {'username': 'newuser', 'verifier': 'abcdefg12345',
                    'salt': 'xyz', 'group_index': 2}
        self.assertEquals(expected, self.passwd.get('newuser'))

    def test_put_existing(self):
        self.passwd.put('jsmith', 'new123', '456', 2)
        expected = {'username': 'jsmith', 'verifier': 'new123',
                    'salt': '456', 'group_index': 2}
        self.assertEquals(expected, self.passwd.get('jsmith'))
    
    def test_put_doesnt_clobber_others(self):
        self.passwd.put('newuser', 'abcdefg12345', 'xyz', 2)
        self.assertEquals(3, self.passwd.get('carol')['group_index'])

    def test_delete(self):
        self.passwd.delete('jsmith')
        self.assertEquals(None, self.passwd.get('jsmith'))

    def test_delete_doesnt_clobber_others(self):
        self.passwd.delete('jsmith')
        self.assertEquals(3, self.passwd.get('carol')['group_index'])
        

class TestSRPUserInfo(TestCase):
    fixtures = ['test.json']

    def test_makes_verifier(self):
        srpinfo = SRPUserInfo(user=User.objects.get(username='jsmith'))
        srpinfo.srp_group = 1024
        srpinfo.set_verifier_from_password("asdf")
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
