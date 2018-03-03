from django import forms
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from catalog import models as cmod



@view_function
def process_request(request):

    EditProduct = cmod.Product.objects.get(id = request.dmp.urlparams[0])
    EditProduct.Status = 'I'
    EditProduct.save()

    return HttpResponseRedirect('/catalog/index')
