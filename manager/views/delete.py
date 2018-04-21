from django import forms
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from manager import models as cmod
from django.contrib.auth.decorators import permission_required


@permission_required('change_product')
@view_function
def process_request(request):

    EditProduct = cmod.Product.objects.get(id = request.dmp.urlparams[0])
    EditProduct.Status = 'I'
    EditProduct.save()

    return HttpResponseRedirect('/manager/index')
