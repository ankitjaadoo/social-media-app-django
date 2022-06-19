from django.test import TestCase
from Posts.models import SNPost
from SNUsers.models import SNUser
 
class PostsTestCase(TestCase):
    def setUp(self):
        user1 = SNUser.objects.create(username="lori",password="sharktank",country="USA")
        SNPost.objects.create(username=user1,post_text="Hi there!")
    def test_create_post(self):
        user1 = SNUser.objects.get(username='lori')
        self.assertEqual("Hi there!",SNPost.objects.get(username=user1).post_text)
