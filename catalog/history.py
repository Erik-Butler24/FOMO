from manager import models as cmod


class LastFiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self,request):

        #get list of ID's from session
        idlist = request.session.get('id')

        #new empty list for product objects
        request.last_five = []

        #add products based on id's in id list

        if idlist:
            for item in idlist:
                request.last_five.append(cmod.Product.objects.get(id = item))

            #subsection the product list
            request.last_five = request.last_five[:5]


        if request.path[0:17] =='/catalog/details/':
            LastProduct = cmod.Product.objects.get(id = request.path[17:])

            #If it's in the list remove it
            if LastProduct in request.last_five:
                request.last_five.remove(LastProduct)

            #else remove the last object
            elif len(request.last_five) > 5:
                request.last_five.pop()


            #and add it again
            request.last_five.insert(0,LastProduct)


        response = self.get_response(request)

        #put the id list back in the session
        idlist = []
        for item in request.last_five:
            idlist.append(item.id)

        request.session['id'] = idlist


        return response
