from django.db import models
from cuser.models import AbstractCUser

class User(AbstractCUser):
    birthdate = models.DateField(blank=True, null=True)

    def getpurchases(self):
        return 0;
