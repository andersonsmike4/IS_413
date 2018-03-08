from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
import math

@view_function
def process_request(request, category: cmod.Category = None):

    categories = cmod.Category.objects.all()

    if category is None:
        qry = cmod.Product.objects.all()
    else:
        qry = cmod.Product.objects.filter(category=category)

    pnum = math.ceil(qry.count()/6)

    print('>>>>>>>>>>>>>>>' + str(pnum))
    context = {
        # sent to index.html:
        'categories': categories,
        'category': category,
        'pnum':pnum
        # sent to index.html and index.js:
        # jscontext(): ,
    }
    return request.dmp.render('index.html', context)

@view_function
def product(request, category: cmod.Category = None, pnum: int=1):
    prod = cmod.Product.objects.filter(category=category)
    products = cmod.Product.objects.all()
    context = {
        # sent to index.product.html:
        'prod': prod,
        'products': products,
        'category': category,
        # sent to index.product.html and index.js:
        # jscontext(): ,
    }
    return request.dmp.render('index.product.html', context)
