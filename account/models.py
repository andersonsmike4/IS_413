from django.db import models
from cuser.models import AbstractCUser

# class Employee(models.Model):
#     firstName = models.TextField(null = True)
#     lastName = models.TextField(null = True)
#     position = models.TextField(null = True)
#     salary = models.IntegerField(null = True)

class User(AbstractCUser):
    birthdate = models.DateTimeField(null = True, blank = True)
    address = models.TextField(null = True, blank = True)
    city = models.TextField(null = True, blank = True)
    state= models.TextField(null = True, blank = True)
    zipcode= models.TextField(null = True, blank = True)

    def get_purchases(self):
        return [ 'Roku Ultimate 4', 'Skis', 'Computer' ]
