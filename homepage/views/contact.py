from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone

@view_function
def process_request(request):
    utc_time = datetime.utcnow()
    context = { }
    if request.method == "POST":
        print(request.POST['first name'])
        print(request.POST['last name'])
    return request.dmp_render('contact.html', context)
