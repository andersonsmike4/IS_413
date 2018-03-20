from catalog import models as cmod


class LastFiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        product_ids = request.session.get('last_prod')
        request.last_five = []
        if product_ids is not None:
            for prod in product_ids:
                request.last_five.insert(0, cmod.Product.objects.get(id=prod))
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        p_ids = []
        for prod in request.last_five[0:6]:
            p_ids.insert(0, prod.id)
            request.session['last_prod'] = p_ids
        return response
