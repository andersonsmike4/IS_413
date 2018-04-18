from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required


@permission_required('catalog.can_edit_product')
@view_function
def process_request(request):
    category = request.GET.get('category', default = 'None')
    product = request.GET.get('product', default = 'None')
    max_price = request.GET.get('max_price', default = 0)
    page = request.GET.get('page', default = 1)

    response = cmod.Product.objects.all().order_by('category', 'name')

    if category != 'None':
        response = response.filter(category__name__icontains=category)
    if product != 'None':
        response = response.filter(name__icontains=product)
    if int(max_price) > 0:
        response = response.filter(price__lte=int(max_price))

    last_number = int(page) * 6
    first_number = last_number - 6
    prods = response[first_number:last_number]

    resp_dict = {'products': []}
    for p in prods:
        data = {
            'category': p.category.name,
            'product': p.name,
            'price': p.price,
        }

        resp_dict['products'].append(data)
    return JsonResponse(resp_dict)
