from django_mako_plus import view_function, jscontext
from manager import models as cmod



@view_function
def process_request(request):

    CategoryID = request.dmp.urlparams[0]

    if CategoryID != "0":
        ProductList = cmod.Product.objects.filter(Category = CategoryID, Status = "A")

    else:
        ProductList = cmod.Product.objects.filter(Status = "A")


    Page = int(request.dmp.urlparams[1])

    ProductList = ProductList[((Page-1)*6):(Page*6)]

    context = {

        'list': ProductList,

    }
    return request.dmp.render('tiles.html', context)

