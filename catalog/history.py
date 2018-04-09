from manager import models as cmod


class LastFiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self,request):

        #get list of recent ID's from session
        idlist = request.session.get('id')

        #new empty list for product objects
        ProdList = []

        #add products based on id's in id list
        if idlist:
            for item in idlist:
                AddedProduct = cmod.Product.objects.get(id = item)
                #only append active products
                if AddedProduct.Status == "A":ProdList.append(AddedProduct)


        #if you're on the product page...
        if request.path[0:17] =='/catalog/details/':
            LastProduct = cmod.Product.objects.get(id = request.path[17:])

            #If it's in the list remove it
            if LastProduct in ProdList:
                ProdList.remove(LastProduct)

            #and add it again
            ProdList.insert(0,LastProduct)

            #show second five
            request.last_five = ProdList[1:6]

        #if anywhere else, show first five
        else:
            request.last_five = ProdList[0:5]

        #trim the list if necessary
        ProdList = ProdList[0:6]

        response = self.get_response(request)

        #put recent id's back into the session (request.session equals the id for each item in prodlist)
        request.session['id'] = [item.id for item in ProdList]

        return response
