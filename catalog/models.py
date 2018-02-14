from django.db import models
from polymorphic.models import PolymorphicModel

# Create your models here.
class Category(models.Model):
    # attributes for category
    name = models.TextField()
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class Product(PolymorphicModel):
    '''a bulk, ind, or rental product'''
    # These are the common attributes of all products

    # TYPE_CHOICES = (
    #     ('BulkProduct', 'Bulk Product' )
    #     ('IndividualProduct', 'Individual Product' )
    #     ('RentalProduct', 'Rental Product' )
    # )

    STATUS = (
      ( 'A', 'Active' ),
      ( 'I', 'Inactive' )
    )

    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.TextField(choices=STATUS, default='A')
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class BulkProduct(Product):
    '''specific for bulk products'''
    TITLE = 'Bulk'
    quantity = models.IntegerField()
    reorder_trigger = models.IntegerField()
    reorder_quantity = models.IntegerField()

class IndividualProduct(Product):
    '''specific for Individual products'''
    TITLE = 'Individual'
    pid = models.TextField()

class RentalProduct(Product):
    '''specific for Rental products'''
    TITLE = 'Rental'
    pid = models.TextField()
    max_rental_days = models.IntegerField(default=0)
    retire_date = models.DateTimeField()
