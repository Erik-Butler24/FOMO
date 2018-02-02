from django.test import TestCase
from account import models as amod
from django.contrib.auth.models import Permission, Group, ContentType


class UserClassTest(TestCase):

    def setUp(self):
        self.u1 = amod.User()
        self.u1.email = 'Homer@simpsons.com'
        self.u1.first_name = 'Homer'
        self.u1.last_name = 'Simpson'
        self.u1.save()

    def test_user_saved(self):
        u2 = amod.User.objects.get(email = 'Homer@simpsons.com')
        self.assertEqual(u2.email, 'Homer@simpsons.com')
        self.assertEqual(u2.first_name,'Homer')
        self.assertEqual(u2.last_name,'Simpson')

    def test_group_permissions(self):
        g1 = Group()
        g1.name = 'Salespeople'
        g1.save()

        g1.permissions.add(Permission.objects.get(id = 1))
        g1.save()

        self.u1.groups.add(g1)
        self.u1.save()

        self.assertTrue(self.u1.has_perm('admin.add_logentry'))

    def test_user_permissions(self):
        self.u1.user_permissions.add(Permission.objects.get(id = 2))
        self.u1.save()

        self.assertTrue(self.u1.has_perm('admin.change_logentry'))

    def test_change_password(self):
        self.u1.set_password('heythere')
        self.assertTrue(self.u1.check_password('heythere'))

    def test_change_info(self):
        self.u1.first_name = 'heythere'
        self.u1.save()
        u2 = amod.User.objects.get(email = 'Homer@simpsons.com')
        self.assertEquals(self.u1.first_name, 'heythere')
        self.assertEquals(u2.first_name, 'heythere')
