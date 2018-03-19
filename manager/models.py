from django.db import models
from polymorphic.models import PolymorphicModel



class Category(models.Model):
    CreateDate = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now=True)
    Name = models.TextField()
    Description = models.TextField()

    def __str__(self):
        return self.Name


class Product(PolymorphicModel):
    TypeChoices = (
        ('B', 'Bulk Product'),
        ('I', 'Individual Product'),
        ('R', 'Rental Product')
    )

    StatusChoices = (
        ('A', 'Active'),
        ('I', 'Inactive'),
    )

    Name = models.TextField()
    Description = models.TextField()
    Category = models.ForeignKey('Category', on_delete=models.CASCADE)
    Price = models.DecimalField(decimal_places=2, max_digits=10)
    CreateDate = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now=True)
    Status = models.TextField(max_length=1, choices=StatusChoices)

    def img_URLs(self):
        return self.images.all()

    def img_URL(self):
        images = self.images.all()
        if not images:
            url = "catalog/media/404.jpg"
        else:
            url = "catalog/media/" + images[0].filename

        return url


class BulkProduct(Product):
    Quantity = models.IntegerField()
    ReorderTrigger = models.IntegerField()
    ReorderQuantity = models.IntegerField()


class IndividualProduct(Product):
    ItemID = models.TextField()


class RentalProduct(Product):
    ItemID = models.TextField()
    MaxRental = models.IntegerField()
    RetireDate = models.DateTimeField()


class ProductImage(models.Model):
    filename = models.TextField()
    product = models.ForeignKey('Product',on_delete=models.CASCADE,related_name='images')
