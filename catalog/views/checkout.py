from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
import math
from django import forms
from django.contrib.auth.decorators import login_required

@login_required
@view_function
def process_request(request, product: cmod.Product = None):

    cart_items = request.user.shopping_cart().active_items()
    # cart_items = request.user.shopping_cart().items.all()
    cart = request.user.shopping_cart()
    tax_product = cmod.Product.objects.get(id=74)
    tax_item = cmod.OrderItem.objects.get(description=tax_product.name)
    context = {
        # sent to index.html:
        'cart_items': cart_items,
        'cart': cart,
        'tax_item': tax_item,
        # sent to index.html and index.js:
        # jscontext(): ,
    }
    return request.dmp.render('cart.html', context)
