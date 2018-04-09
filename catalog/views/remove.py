from django_mako_plus import view_function
from manager import models as cmod
from account import models as amod
from django.http import HttpResponseRedirect

@view_function
def process_request(request, OrderItem:cmod.OrderItem):

    OrderItem.status = "Deleted"
    OrderItem.save()
    return HttpResponseRedirect('/catalog/cart')

