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
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = createProductForm()

    context = {
        'form': form,

    }
    return request.dmp_render('createCategory.html', context)


class createProductForm(forms.Form):
    Name = forms.CharField(label='Name', required=True)
    Description = forms.CharField(label='Description', required=True)



    def clean(self):
        name = self.cleaned_data.get('name')
        if cmod.Category.objects.filter(Name = name):
            raise forms.ValidationError('There is already an account with that Email')


    def commit(self,request):
        newCategory = cmod.Category()
        newCategory.Name = self.cleaned_data.get('Name')
        newCategory.Description = self.cleaned_data.get('Description')
        newCategory.save()
