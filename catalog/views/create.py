from django import forms
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from catalog import models as cmod



@view_function
def process_request(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = createProductForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            createProductForm.commit(form, request)
            return HttpResponseRedirect('/catalog/index')

    # if a GET (or any other method) we'll create a blank form

    elif request.dmp.urlparams[0]:
        EditProduct = cmod.Product.objects.get(id = request.dmp.urlparams[0])
        if EditProduct.__class__.__name__ == 'BulkProduct':
            form = createProductForm(initial={'ProductType': 'B',
                                              'Quantity': EditProduct.Quantity,
                                              'ReorderTrigger': EditProduct.ReorderTrigger,
                                              'ReorderQuantity': EditProduct.ReorderQuantity,
                                              'Status': EditProduct.Status,
                                              'Name': EditProduct.Name,
                                              'Category': EditProduct.Category,
                                              'Description': EditProduct.Description,
                                              'Price': EditProduct.Price})

        elif EditProduct.__class__.__name__ == 'IndividualProduct':
            form = createProductForm(initial={'ProductType': 'I',
                                              'ItemID': EditProduct.ItemID,
                                              'Status': EditProduct.Status,
                                              'Name': EditProduct.Name,
                                              'Category': EditProduct.Category,
                                              'Description': EditProduct.Description,
                                              'Price': EditProduct.Price})

        elif EditProduct.__class__.__name__ == 'RentalProduct':
            form = createProductForm(initial={'ProductType': 'R',
                                              'ItemID': EditProduct.ItemID,
                                              'MaxRental': EditProduct.MaxRental,
                                              'RetireDate': EditProduct.RetireDate,
                                              'Status': EditProduct.Status,
                                              'Name': EditProduct.Name,
                                              'Category': EditProduct.Category,
                                              'Description': EditProduct.Description,
                                              'Price': EditProduct.Price})

    else:
        form = createProductForm()

    context = {
        'form': form,

    }
    return request.dmp.render('create.html', context)


class createProductForm(forms.Form):
    ProductType = forms.ChoiceField(label='Product Type', choices=cmod.Product.TypeChoices)
    Status = forms.ChoiceField(label='Status', choices=cmod.Product.StatusChoices)
    Name = forms.CharField(label='Name', required=True)
    Category = forms.ModelChoiceField(label='Category', queryset=cmod.Category.objects)
    Description = forms.CharField(label='Description', required=True)
    Price = forms.DecimalField(label='Price', required=True)
    Quantity = forms.IntegerField(label='Quantity',required=False)
    ReorderTrigger = forms.IntegerField(label='Reorder Trigger', required=False)
    ReorderQuantity = forms.IntegerField(label='Reorder Quantity', required=False)
    ItemID = forms.IntegerField(label='Item ID', required=False)
    MaxRental = forms.IntegerField(label='Max Rental Days', required=False)
    RetireDate = forms.DateTimeField(label='Retire Date', required=False)

    def commit(self,request):
        if request.dmp.urlparams[0]:
            newProduct = cmod.Product.objects.get(id = request.dmp.urlparams[0])
        else: newProduct = None

        if self.cleaned_data.get('ProductType') == 'B':
                if newProduct is None: newProduct = cmod.BulkProduct()
                newProduct.Quantity = self.cleaned_data.get('Quantity')
                newProduct.ReorderTrigger = self.cleaned_data.get('ReorderTrigger')
                newProduct.ReorderQuantity = self.cleaned_data.get('ReorderQuantity')

        if self.cleaned_data.get('ProductType') == 'I':
                if newProduct is None: newProduct = cmod.IndividualProduct()
                newProduct.ItemID = self.cleaned_data.get('ItemID')

        if self.cleaned_data.get('ProductType') == 'R':
                if newProduct is None: newProduct = cmod.RentalProduct()
                newProduct.ItemID = self.cleaned_data.get('ItemID')
                newProduct.MaxRental = self.cleaned_data.get('MaxRental')
                newProduct.RetireDate = self.cleaned_data.get('RetireDate')

        newProduct.Status = self.cleaned_data.get('Status')
        newProduct.Name = self.cleaned_data.get('Name')
        newProduct.Category = self.cleaned_data.get('Category')
        newProduct.Description = self.cleaned_data.get('Description')
        newProduct.Price = self.cleaned_data.get('Price')
        newProduct.save()

    def clean(self):
        if self.cleaned_data.get('ProductType') == 'B':
                if not self.cleaned_data.get('Quantity'):
                    raise forms.ValidationError('Quantity field is required')
                if not self.cleaned_data.get('ReorderTrigger'):
                    raise forms.ValidationError('Reorder Trigger field is required')
                if not self.cleaned_data.get('ReorderQuantity'):
                    raise forms.ValidationError('Reorder Quantity field is required')

        if self.cleaned_data.get('ProductType') == 'I':
                if not self.cleaned_data.get('ItemID'):
                    raise forms.ValidationError('Item ID field is required')

        if self.cleaned_data.get('ProductType') == 'R':
                if not self.cleaned_data.get('ItemID'):
                    raise forms.ValidationError('Item ID field is required')
                if not self.cleaned_data.get('MaxRental'):
                    raise forms.ValidationError('Max Rental days field is required')
                if not self.cleaned_data.get('RetireDate'):
                    raise forms.ValidationError('Retire Date field is required')
