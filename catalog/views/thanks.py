from django_mako_plus import view_function
from manager import models as cmod
from django.contrib.auth.decorators import permission_required

@view_function
def process_request(request):

    context = {
        'list': cmod.Category.objects.all(),
        'cart_size':0,

    }
    return request.dmp.render('thanks.html', context)

