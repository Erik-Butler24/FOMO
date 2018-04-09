from django_mako_plus import view_function
from manager import models as cmod
from account import models as amod
from django.http import HttpResponseRedirect

@view_function
def process_request(request, product:cmod.Product):

    if request.user.is_authenticated:
        cart = amod.User.objects.get(email = request.user).get_shopping_cart()
        cartsize = cart.num_items()
    else:
        return HttpResponseRedirect('/account/login')

    quantity = int(request.POST["PurchaseQuantity"])

    if product.__class__.__name__ == 'BulkProduct' and product.Quantity < quantity: return HttpResponseRedirect('/catalog/details/' + str(product.id))

    if cart.active_items().filter(product = product):
        updateitem = cart.active_items().get(product = product)
        updateitem.status = "active"
        updateitem.quantity = quantity
        updateitem.save()
        return HttpResponseRedirect('/catalog/cart')

    NewOrderLine = cmod.OrderItem()
    NewOrderLine.description = product.Description
    NewOrderLine.price = product.Price
    NewOrderLine.quantity = quantity
    NewOrderLine.extended = quantity*product.Price
    NewOrderLine.order_id = cart.id
    NewOrderLine.product = product
    NewOrderLine.save()


    context = {
        'list': cmod.Category.objects.all(),
        'cart': cart,
        'cart_size': cartsize
    }
    return HttpResponseRedirect('/catalog/cart')

