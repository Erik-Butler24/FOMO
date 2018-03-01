from django.conf import settings
from django_mako_plus import view_function

@view_function
def process_request(request):
    return request.dmp.render('FAQ.html')
