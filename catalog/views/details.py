from django_mako_plus import view_function, jscontext
from manager import models as cmod



@view_function
def process_request(request, product:cmod.Product):
    #The get(urlparams[0])happens right there^^


    context = {
        'list': cmod.Category.objects.all(),
        'product': product,
        jscontext('ProdName'): product.Name,
        jscontext('CatName'): product.Category.Name,
    }
    return request.dmp.render('details.html', context)

