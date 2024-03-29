from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django.contrib.auth.decorators import permission_required

@permission_required('catalog.can_edit_product')
@view_function
def process_request(request):
    utc_time = datetime.utcnow()
    print(request.dmp.page)
    context = {
        # sent to index.html:
        'utc_time': utc_time,
        # sent to index.html and index.js:
        jscontext('utc_epoch'): utc_time.timestamp(),
    }
    return request.dmp.render('index.html', context)
