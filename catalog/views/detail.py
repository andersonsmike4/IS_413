from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
import math

@view_function
def process_request(request, product: cmod.Product = None):


    context = {
        # sent to index.html:
        'product': product,
        # sent to index.html and index.js:
        # jscontext(): ,
    }
    return request.dmp.render('detail.html', context)
