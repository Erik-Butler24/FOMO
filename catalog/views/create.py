from django import forms
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from catalog import models as cmod
import re
from django.contrib.auth import authenticate, login



@view_function
def process_request(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = createProductForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            createProductForm.commit(form, request)
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = createProductForm()

    context = {
        'form': form,

    }
    return request.dmp_render('create.html', context)


class createProductForm(forms.Form):
    ProductType = forms.ChoiceField(label='Product Type', choices=cmod.Product.TypeChoices)
    Status = forms.ChoiceField(label='Status', choices=cmod.Product.StatusChoices)
    Name = forms.CharField(label='Name', required=True)
    Category = forms.ModelChoiceField(label='Category', queryset=cmod.Category.objects)
    Description = forms.CharField(label='Description', required=True)
    Price = forms.CharField(label='Price', required=True)
    Quantity = forms.IntegerField(label='Quantity')
    ReorderTrigger = forms.IntegerField(label='Reorder Trigger')
    ReorderQuantity = forms.IntegerField(label='Reorder Quantity')
    MaxRental = forms.IntegerField(label='Max Rental')
    RetireDate = forms.DateTimeField(label='Retire Date')



    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2 and password is not None:
            raise forms.ValidationError('Passwords do not match')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters')
        if re.search('[0-9]', password) is None:
            raise forms.ValidationError('Password must contain a number')
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        print(email)
        if cmod.User.objects.filter(email = email):
            raise forms.ValidationError('There is already an account with that Email')
        return email

    def commit(self,request):
            if self.cleaned_data.get('ProductType') == 'B':
                newProduct = cmod.BulkProduct()
                newProduct.Quantity = self.cleaned_data.get('Quantity')
                newProduct.ReorderTrigger = self.cleaned_data.get('ReorderTrigger')
                newProduct.ReorderQuantity = self.cleaned_data.get('ReorderQuantity')

            if self.cleaned_data.get('ProductType') == 'I':
                newProduct = cmod.IndividualProduct()

            if self.cleaned_data.get('ProductType') == 'R':
                newProduct = cmod.RentalProduct()
                newProduct.MaxRental = self.cleaned_data.get('MaxRental')
                newProduct.RetireDate = self.cleaned_data.get('RetireDate')

            newProduct.Status = self.cleaned_data.get('Status')
            newProduct.Name = self.cleaned_data.get('Name')
            newProduct.Category = self.cleaned_data.get('Category')
            newProduct.Description = self.cleaned_data.get('Description')
            newProduct.Price = self.cleaned_data.get('Price')
            newProduct.save()
