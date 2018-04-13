from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
import math
from django import forms
from django.http import HttpResponseRedirect


@view_function
def process_request(request):
    # direct user to login if they are not logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login/')


    products = cmod.Product.objects.all()
    cart_items = request.user.get_shopping_cart().active_items()
    # cart_items = request.user.get_shopping_cart().items.all()
    cart = request.user.get_shopping_cart()
    # redirect to catalog if there are no items inthe cart
    if cart.total_price == 0:
        return HttpResponseRedirect('/catalog/index/')

    tax_product = cmod.Product.objects.get(id=74)
    tax_item = cmod.OrderItem.objects.get(description=tax_product.name)
    context = {
        # sent to index.html:
        'cart_items': cart_items,
        'cart': cart,
        'tax_item': tax_item,
        'products': products,
        # sent to index.html and index.js:
        # jscontext(): ,
    }
    return request.dmp.render('cart.html', context)
