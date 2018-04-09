from django.db import models
from cuser.models import AbstractCUser
from manager import models as cmod
from django.core.exceptions import ObjectDoesNotExist

class User(AbstractCUser):
    birthdate = models.DateField(blank=True, null=True)

    def get_shopping_cart(self):
        try:
            cart = cmod.Order.objects.get(status = "cart", user_id = self.id)
        except ObjectDoesNotExist:
            newcart = cmod.Order()
            newcart.user_id = self.id
            newcart.save()
            cart = cmod.Order.objects.get(status = "cart", user_id = self.id)

        return cart
