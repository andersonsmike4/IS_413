from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone

@view_function
def process_request(request):
    if request.method == 'POST':
        print(request.POST['Name'])
        print(request.POST['Email'])
        print(request.POST['Phone'])
        print(request.POST['Message'])    
    context = {

    }
    return request.dmp.render('contact.html', context)
