from django_mako_plus import view_function
from catalog import models as cmod



@view_function
def process_request(request):

    context = {
        'list': cmod.Product.objects.filter(Status = 'A'),

    }
    return request.dmp.render('index.html', context)

