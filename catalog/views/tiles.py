from django_mako_plus import view_function, jscontext
from manager import models as cmod



@view_function
def process_request(request):

    CategoryID = request.dmp.urlparams[0]

    if CategoryID != "0":
        print(CategoryID)
        ProductList = cmod.Product.objects.filter(Category = CategoryID)

    else:
        ProductList = cmod.Product.objects.all()




    context = {

        'list': ProductList,

    }
    return request.dmp.render('tiles.html', context)

