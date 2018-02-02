from django.test import TestCase
from account import models as amod

class AnimalTestCase(TestCase):
    def setUp(self):
        u1 = amod.User()
        u1.email = 'Homer@simpsons.com'
        u1.first_name = 'Homer'
        u1.last_name = 'Simpson'
        u1.save()



    def test_user_saved(self):
        u2 = amod.User.objects.get(email = 'Homer@simpsons.com')
        self.assertEqual(u2.email, 'Homer@simpsons.com')
        self.assertEqual(u2.first_name,'Homer')
        self.assertEqual(u2.last_name,'Simpson')

