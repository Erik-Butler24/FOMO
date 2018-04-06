from django_mako_plus import view_function
from manager import models as cmod
from django.contrib.auth.decorators import permission_required


@permission_required('change_product')
@view_function
def process_request(request):

    context = {
        'list': cmod.Product.objects.filter(Status = 'A'),

    }
    return request.dmp.render('index.html', context)

