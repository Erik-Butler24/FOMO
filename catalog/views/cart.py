from django_mako_plus import view_function
from manager import models as cmod
from account import models as amod
from django.http import HttpResponseRedirect

@view_function
def process_request(request):

    if request.user.is_authenticated:
        cart = amod.User.objects.get(email = request.user).get_shopping_cart()
        cartsize = cart.num_items()
    else:
        return HttpResponseRedirect('/account/login')

    cart.recalculate()
    context = {
        'list': cmod.Category.objects.all(),
        'cart': cart,
        'cart_size': cartsize

    }
    return request.dmp.render('cart.html', context)

