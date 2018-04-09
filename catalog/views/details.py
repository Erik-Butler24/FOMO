from django_mako_plus import view_function, jscontext
from manager import models as cmod
from account import models as amod



@view_function
def process_request(request, product:cmod.Product):
    #The get(urlparams[0])happens right there^^

    if request.user.is_authenticated:
        cart = amod.User.objects.get(email = request.user).get_shopping_cart()
        cartsize = cart.num_items()
    else:
        cartsize = 0


    context = {
        'cart_size': cartsize,
        'list': cmod.Category.objects.all(),
        'product': product,
        jscontext('ProdName'): product.Name,
        jscontext('CatName'): product.Category.Name,
    }
    return request.dmp.render('details.html', context)

