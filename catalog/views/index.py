from django_mako_plus import view_function, jscontext
from manager import models as cmod
import math
from account import models as amod



@view_function
def process_request(request):

    if not request.dmp.urlparams[0] or request.dmp.urlparams[0] == "0":
        CatName = None
        CatID = 0
        MaxPages = math.ceil((cmod.Product.objects.filter(Status = 'A').count())/6)

    else:

        CatName = cmod.Category.objects.get(id = request.dmp.urlparams[0]).Name
        CatID = cmod.Category.objects.get(id = request.dmp.urlparams[0]).id
        MaxPages = math.ceil((cmod.Product.objects.filter(Category = CatID, Status = 'A').count())/6)

    if request.user.is_authenticated:
        cart = amod.User.objects.get(email = request.user).get_shopping_cart()
        cartsize = cart.num_items()
    else:
        cartsize = 0


    context = {
        'list': cmod.Category.objects.all(),
        'cart_size': cartsize,
        jscontext('CatID'): CatID,
        jscontext('CatName'): CatName,
        jscontext('Pagenum'): 1,
        jscontext('MaxPages'): MaxPages,

    }
    return request.dmp.render('index.html', context)

