from django.test import TestCase
from SNUsers.models import SNUser
 
class SNUserTestCase(TestCase):
    def setUp(self):      
        SNUser.objects.create(username="mark_cuban",
                             password="sharktank",
                             country="USA")
    def test_create(self):
        self.assertEqual("USA",
                      SNUser.objects.get(username="mark_cuban").country)
    def test_api_login(self):
     client = Client()
     response = client.post('/login/', 
                {'username':'mark_cuban'},format='json')
                 self.assertEqual(200,response.status_code)