import unittest, tempfile

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
