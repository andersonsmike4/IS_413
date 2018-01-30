from django.test import TestCase
from account import models as amod

# Create your tests here.
class UserClassTest(TestCase):
    def setUp(self):
        # this runs beofre each function
        self.u1 = amod.User()
        self.u1.first_name = 'Lisa'
        self.u1.last_name = 'Simpson'
        self.u1.email = 'lisa@simpsons.com'
        self.u1.set_password('password')
        self.u1.address = '123 Fake Ln'
        self.u1.city = 'Springfield'
        self.u1.state = 'State'
        self.u1.zipcode = '12345'
        self.u1.birthdate = '2018-01-30'
        self.u1.save()


    def test_load_save(self):
        '''Test creating, saving, and reloading a user'''


        u2 = amod.User.objects.get(email = 'lisa@simpsons.com')
        self.assertEqual(self.u1.first_name, u2.first_name)
        self.assertEqual(self.u1.last_name, u2.last_name)
        self.assertEqual(self.u1.email, u2.email)
        self.assertEqual(self.u1.password, u2.password)
        self.assertTrue(u2.check_password('password'))


    # def test_adding_groups(self):
    #     '''Test adding a few groups'''

    def test_login(self):
        amod.User.objects.get(email = 'lisa@simpsons.com')
