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

