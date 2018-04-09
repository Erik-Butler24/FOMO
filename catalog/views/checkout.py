from django import forms
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from manager import models as cmod
import stripe



@view_function
def process_request(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CheckoutForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            CheckoutForm.commit(form, request)
            stripe.api_key = "sk_test_wadBVqwzbMzhY9jhgE5QqmJW"

            # Token is created using Checkout or Elements!
            # Get the payment token ID submitted by the form:
            token = form.cleaned_data.get('stripeToken')

            charge = stripe.Charge.create(
                amount=999,
                currency='usd',
                description='Example charge',
                source=token,
            )
            return HttpResponseRedirect('/catalog/thanks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'list': cmod.Category.objects.all(),
        'cart': cmod.Product.objects.filter(Status = 'A'),

    }
    return request.dmp.render('checkout.html', context)


class CheckoutForm(forms.Form):
    address = forms.CharField(label='Address')
    address2 = forms.CharField(label='Address 2', required=False)
    city = forms.CharField(label='City')
    state = forms.CharField(label='State')
    country = forms.CharField(label='Country')
    zip = forms.CharField(label='zip')
    stripeToken = forms.CharField(label='stripeToken', required=False, widget = forms.HiddenInput())

    def clean(self):
        print("success")

    def commit(self, request):
        print("success")
