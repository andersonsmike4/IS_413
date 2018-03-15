from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
import math

@view_function
def process_request(request, category: cmod.Category = None):
    
    categories = cmod.Category.objects.all()
    id=0
    if category is None:
        qry = cmod.Product.objects.filter(status='A')
    else:
        qry = cmod.Product.objects.filter(category=category, status='A')
        id = category.id

    total_pages = math.ceil(qry.count()/6)

    context = {
        # sent to index.html:
        'categories': categories,
        'category': category,
        jscontext('categoryid'): id,
        jscontext('total_pages'):total_pages,
        # sent to index.html and index.js:
        # jscontext(): ,
    }
    return request.dmp.render('index.html', context)

@view_function
def product(request, category: cmod.Category = None, pnum: int=1):

    if category is None:
        products = cmod.Product.objects.filter(status='A')
    else:
        products = cmod.Product.objects.filter(category=category, status='A')
    last_number = pnum * 6
    first_number = last_number - 6
    products = products[first_number:last_number]
    context = {
        # sent to index.product.html:
        'products': products,
        'category': category,
        # sent to index.product.html and index.js:
        # jscontext(): ,
    }
    return request.dmp.render('index.product.html', context)
