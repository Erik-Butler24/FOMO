from django import forms
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from manager import models as cmod
from account import models as amod



@view_function
def process_request(request):

    cart = amod.User.objects.get(email = request.user).get_shopping_cart()
    cartsize = cart.num_items()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CheckoutForm(request.POST, request=request)
        # check whether it's valid:
        if form.is_valid():
            CheckoutForm.commit(form, request)
            return HttpResponseRedirect('/catalog/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'list': cmod.Category.objects.all(),
        'cart': cart,
        'cart_size': cartsize,

    }
    return request.dmp.render('checkout.html', context)


class CheckoutForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CheckoutForm, self).__init__(*args, **kwargs)

    address = forms.CharField(label='Address')
    address2 = forms.CharField(label='Address 2', required=False)
    city = forms.CharField(label='City')
    state = forms.CharField(label='State')
    country = forms.CharField(label='Country')
    zip = forms.CharField(label='zip')
    stripeToken = forms.CharField(label='stripeToken', required=False, widget = forms.HiddenInput())

    def clean(self):
        cart = amod.User.objects.get(email = self.request.user).get_shopping_cart()
        print("cleaning")
        cart.finalize(self.cleaned_data.get('stripeToken'))


    def commit(self, request):
        print("Success")

