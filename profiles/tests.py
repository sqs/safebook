from django.test import TestCase

class IndexTest(TestCase):
    fixtures = ['test.json']
    
    def test_get(self):
        res = self.client.get('/')
        self.assertContains(res, '<h1>Safebook</h1>')
        self.assertContains(res, 'jsmith')
    
class DetailTest(TestCase):
    fixtures = ['test.json']
    
    def test_get_detail(self):
        res = self.client.get('/jsmith')
        self.assertContains(res, '<h1>jsmith</h1>')
    
    def test_get_unknown_user(self):
        res = self.client.get('/unknownuser')
        self.assertEquals(res.status_code, 404)

class BaseTemplateTest(TestCase):
    fixtures = ['test.json']

    def test_show_logged_in_user(self):
        res = self.client.get('/', SSL_SRP_USER='user')
        self.assertContains(res, 'you are user')

    def test_not_logged_in(self):
        res = self.client.get('/')
        self.assertContains(res, 'not logged in')
