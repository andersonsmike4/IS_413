from django.test import TestCase
from account import models as amod
from django.test import Client
from django.contrib.auth.models import Group, Permission, ContentType
from django.contrib import auth

# Create your tests here.
class UserClassTest(TestCase):

    # use this to create a user that can be used for every class
    fixtures = ['data.yaml']

    def setUp(self):
        # use this line to get the user from the fixtures file
        # self.u1 = amod.User.objects.get(email='homer@simpson.com')

        # this runs before each function
        self.u1 = amod.User()
        self.u1.first_name = 'Lisa'
        self.u1.last_name = 'Simpson'
        self.u1.email = 'lisa@simpsons.com'
        self.u1.set_password('password')
        self.u1.address = '123 Fake Ln'
        self.u1.city = 'Springfield'
        self.u1.state = 'State'
        self.u1.zipcode = '12345'
        self.u1.save()


    def test_load_save(self):
        '''Test creating, saving, and reloading a user'''
        u2 = amod.User.objects.get(email = 'lisa@simpsons.com')
        self.assertEqual(self.u1.first_name, u2.first_name)
        self.assertEqual(self.u1.last_name, u2.last_name)
        self.assertEqual(self.u1.email, u2.email)
        self.assertEqual(self.u1.password, u2.password)
        self.assertEqual(self.u1.address, u2.address)
        self.assertEqual(self.u1.city, u2.city)
        self.assertEqual(self.u1.state, u2.state)
        self.assertEqual(self.u1.zipcode, u2.zipcode)
        self.assertTrue(u2.check_password('password'))

    def test_groups_permissions(self):
        '''Test permissions and adding groups to users'''
        g1 = Group()
        g1.name = 'Salespeople'
        # you must save before you add test_groups_permissions
        g1.save()
        g1.permissions.add(Permission.objects.get(id=1))

        # prints out all available test_groups_permissions
        # for p in Permission.objects.all():
        #     print('Codename: ' + p.codename)
        #     print('Name: ' + p.name)
        #     print('ContentType: ' + str(p.content_type))
        #     this is a pretty bad idea: self.u1.user_permissions.add(p)

        # create a permission
        p = Permission()
        p.codename = 'change_product_price'
        p.name = 'Change the price of a product'
        p.content_type = ContentType.objects.get(id=1)
        p.save()

        # add permission to groups
        g1.permissions.add(Permission.objects.get(codename='change_product_price'))
        g1.save()

        # add user to group
        self.u1.groups.add(g1)
        self.u1.save()

        # check to see if the group has the new permissions
        self.assertTrue(self.u1.groups.filter(name = 'Salespeople'))
        self.assertTrue(self.u1.has_perm('admin.change_product_price'))

    def test_user_permissions(self):
        '''Add permissions to users and test permissions'''
        p = Permission()
        p.codename = 'change_product_price'
        p.name = 'Change the price of a product'
        p.content_type = ContentType.objects.get(id=1)
        p.save()

        p1 = Permission()
        p1.codename = 'change_product_name'
        p1.name = 'Change the name of a product'
        p1.content_type = ContentType.objects.get(id=1)
        p1.save()

        # add permission to user
        self.u1.user_permissions.add(p)
        self.u1.user_permissions.add(p1)
        self.u1.save()

        self.assertTrue(self.u1.has_perm('admin.change_product_price'))
        self.assertTrue(self.u1.has_perm('admin.change_product_name'))

    def test_login(self):
        '''Test login'''
        c = Client()
        a = c.login(email = self.u1.email, password = 'password')
        self.assertTrue(a)
        u = auth.get_user(c)

        self.assertTrue(u.is_authenticated)
        self.assertFalse(u.is_anonymous)

    def test_logout(self):
        '''Test logout'''
        c = Client()
        # login in first
        a = c.login(email = self.u1.email, password = 'password')
        self.assertTrue(a)
        u = auth.get_user(c)

        self.assertTrue(u.is_authenticated)
        self.assertFalse(u.is_anonymous)

        # now logout
        a = c.logout()
        self.assertFalse(a)
        u = auth.get_user(c)

        self.assertFalse(u.is_authenticated)
        self.assertTrue(u.is_anonymous)

    def test_password(self):
        u2 = amod.User.objects.get(email = 'lisa@simpsons.com')
        # check to see if the passwords are the same
        self.assertEqual(self.u1.password, u2.password)

        self.assertTrue(u2.check_password('password'))

    def test_field_change(self):
        # change the fields in u1 and save to the db
        self.u1.first_name = 'Bob'
        self.u1.last_name = 'Smith'
        self.u1.email = 'bob@smith.com'
        self.u1.save()

        # check to make sure it was updated in the database
        u2 = amod.User.objects.get(id=self.u1.id)
        self.assertEqual(u2.first_name, 'Bob')
        self.assertEqual(u2.last_name, 'Smith')
        self.assertEqual(u2.email, 'bob@smith.com')
