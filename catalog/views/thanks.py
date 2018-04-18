from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
import math
from django import forms

from django.http import HttpResponseRedirect


@view_function
def process_request(request, cart:cmod.Order):
    tax_product = cmod.Product.objects.get(id=74)
    items = cart.active_items().exclude(description=tax_product.name)
    tax = cart.items.get(description=tax_product.name)
    print('>>>>>>>>>>>.cart yay i have items', items)
    context = {
        # sent to index.html:
        'cart': cart,
        'items': items,
        'tax': tax,
    }
    return request.dmp.render('thanks.html', context)
    # return request.dmp.render('cart.html', context)
