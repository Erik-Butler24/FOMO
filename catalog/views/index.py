from django_mako_plus import view_function
from manager import models as cmod



@view_function
def process_request(request):

    context = {
        'list': cmod.Category.objects.all(),

    }
    return request.dmp.render('index.html', context)

