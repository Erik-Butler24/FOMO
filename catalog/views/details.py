from django_mako_plus import view_function, jscontext
from manager import models as cmod
import math



@view_function
def process_request(request):
    product =  cmod.Product.objects.get(id = request.dmp.urlparams[0])


    context = {
        'list': cmod.Category.objects.all(),
        'product': product,
        jscontext('ProdName'): product.Name,
        jscontext('CatName'): product.Category.Name,
    }
    return request.dmp.render('details.html', context)

