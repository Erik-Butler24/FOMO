from django_mako_plus import view_function, jscontext
from manager import models as cmod



@view_function
def process_request(request):

    if not request.dmp.urlparams[0] or request.dmp.urlparams[0] == "0":
        CatName = None
        CatID = 0

    else:

        CatName = cmod.Category.objects.get(id = request.dmp.urlparams[0]).Name
        CatID = cmod.Category.objects.get(id = request.dmp.urlparams[0]).id


    context = {
        'list': cmod.Category.objects.all(),
        jscontext('CatID'): CatID,
        jscontext('CatName'): CatName,
        jscontext('Pagenum'): 1,

    }
    return request.dmp.render('index.html', context)

