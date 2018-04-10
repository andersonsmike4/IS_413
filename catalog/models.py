from django.db import models, transaction
from django.conf import settings
from django.forms.models import model_to_dict
from polymorphic.models import PolymorphicModel
from decimal import Decimal
from datetime import datetime
import stripe

# Create your models here.
class Category(models.Model):
    '''Product categories'''
    name = models.TextField()
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Product(PolymorphicModel):
    '''a bulk, ind, or rental product'''
    # These are the common attributes of all products
    TYPE_CHOICES = (
        ('', '--Select Product Type--' ),
        ('BulkProduct', 'Bulk Product' ),
        ('IndividualProduct', 'Individual Product' ),
        ('RentalProduct', 'Rental Product' )
    )

    STATUS_CHOICES = (
      ( 'A', 'Active' ),
      ( 'I', 'Inactive' )
    )

    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.TextField(choices=STATUS_CHOICES, default='A')
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def image_url(self):
        '''returns the first image'''
        pi = self.images.first()
        url = settings.STATIC_URL + 'catalog/media/products/'
        if pi is None:
            url += 'image_unavailable.gif'
        else:
            url += pi.filename
        return url

    def image_urls(self):
        '''returns a list of images'''
        image_list = []
        # go through all the images
        for pi in self.images.all():
            url = settings.STATIC_URL + 'catalog/media/products/'
            # determine if there is an image
            if pi is None:
                url += 'image_unavailable.gif'
            else:
                url += pi.filename
            # add the url to the list
            image_list.append(url)
        return image_list

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
    retire_date = models.DateTimeField(null=True, blank=True)

class ProductImage(models.Model):
    '''contains product images'''
    filename = models.TextField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class Order(models.Model):
    '''An order in the system'''
    STATUS_CHOICES = (
        ( 'cart', 'Shopping Cart' ),
        ( 'payment', 'Payment Processing' ),
        ( 'sold', 'Finalized Sale' ),
    )
    order_date = models.DateTimeField(null=True, blank=True)
    name = models.TextField(blank=True, default="Shopping Cart")
    status = models.TextField(choices=STATUS_CHOICES, default='cart', db_index=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    user = models.ForeignKey('account.User', related_name='orders',  on_delete=models.CASCADE)
    # shipping information
    ship_date = models.DateTimeField(null=True, blank=True)
    ship_tracking = models.TextField(null=True, blank=True)
    ship_name = models.TextField(null=True, blank=True)
    ship_address = models.TextField(null=True, blank=True)
    ship_city = models.TextField(null=True, blank=True)
    ship_state = models.TextField(null=True, blank=True)
    ship_zip_code = models.TextField(null=True, blank=True)

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'Order {}: {}: {}'.format(self.id, self.user.get_full_name(), self.total_price)


    def active_items(self, include_tax_item=True):
        '''Returns the active items on this order'''
        # create a query object (filter to status='active')
        tax_product = Product.objects.get(id=74)
        return self.items.filter(status='active').exclude(description=tax_product.name).all()
        # if we aren't including the tax item, alter the
        # query to exclude that OrderItem
        # I simply used the product name (not a great choice,
        # but it is acceptable for credit)


    def get_item(self, product, create=False):
        '''Returns the OrderItem object for the given product'''
        item = OrderItem.objects.filter(order=self, product=product).first()
        if item is None and create:
            item = OrderItem.objects.create(order=self, product=product, price=product.price, quantity=0)
        elif create and item.status != 'active':
            item.status = 'active'
            item.quantity = 0
        if item is not None:
            item.recalculate()
            item.save()
        item.recalculate()
        item.save()
        return item


    def num_items(self):
        '''Returns the number of items in the cart'''
        return sum(self.active_items(include_tax_item=False).values_list('quantity', flat=True))


    def recalculate(self):
        '''
        Recalculates the total price of the order,
        including recalculating the taxable amount.

        Saves this Order and all child OrderLine objects.
        '''
        # iterate the order items (not including tax item) and get the total price
        # call recalculate on each item

        tax_product = Product.objects.get(id=74)
        order_items = self.items.all()
        total_price = 0
        create = True
        for i in order_items:
            i.recalculate()
            total_price += i.extended
            if i.description == tax_product.name:
                create = False


        # update/create the tax order item (calculate at 7% rate)

        # sales_tax_item = self.get_item(tax_product)
        if create:
            tax_item = OrderItem()
            tax_item.price = 0
            tax_item.description = tax_product.name
            tax_item.quantity = 1
            tax_item.order = self
            tax_item.product = tax_product
            print('>>>>>>>>>>>>>>>>>>>', create)
            tax_item.save()


        tax_item = self.get_item(tax_product, create)
        tax_item.price = Decimal(total_price) * Decimal(0.07)
        tax_item.recalculate()
        # tax_item.save()
        # update the total and save
        self.total_price = total_price + tax_item.price
        self.save()

    def finalize(self, stripe_charge_token):
        '''Runs the payment and finalizes the sale'''
        # with transaction.atomic():
            # recalculate just to be sure everything is updated

            # check that all products are available

            # contact stripe and run the payment (using the stripe_charge_token)

            # finalize (or create) one or more payment objects

            # set order status to sold and save the order

            # update product quantities for BulkProducts
            # update status for IndividualProducts


class OrderItem(PolymorphicModel):
    '''A line item on an order'''
    STATUS_CHOICES = (
        ( 'active', 'Active' ),
        ( 'deleted', 'Deleted' ),
    )
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    status = models.TextField(choices=STATUS_CHOICES, default='active', db_index=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    quantity = models.IntegerField(default=0)
    extended = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'OrderItem {}: {}: {}'.format(self.id, self.product.name, self.extended)


    def recalculate(self, product=None):
        '''Updates the order item's price, quantity, extended'''
        # update the price if it isn't already set and we have a product
        if product is not None and self.price is not None:
            self.price = product.price
        # default the quantity to 1 if we don't have a quantity set

        # calculate the extended (price * quantity)
        self.extended = self.price * self.quantity
        # save the changes
        self.save()

class Payment(models.Model):
    '''A payment on a sale'''
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2) # max number is 999,999.99
    validation_code = models.TextField(null=True, blank=True)
