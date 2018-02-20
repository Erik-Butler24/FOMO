from django.db import models
from polymorphic.models import PolymorphicModel


class Category(models.Model):
    CreateDate = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now=True)
    Name = models.TextField()
    Description = models.TextField()


class Product(PolymorphicModel):
    TypeChoices = (
        ('B', 'Bulk Product'),
        ('I', 'Individual Product'),
        ('R', 'Retal Product')
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
    ProductType = models.CharField(max_length=1, choices=TypeChoices)
    Status = models.CharField(max_length=1, choices=StatusChoices)


class BulkProduct(Product):
    Quantity = models.IntegerField()
    ReorderTrigger = models.IntegerField()
    ReorderQuantity = models.IntegerField()


class IndividualProduct(Product):
    ItemID = models.IntegerField()


class RentalProduct(Product):
    ItemID = models.IntegerField()
    MaxRental = models.IntegerField()
    RetireDate = models.DateTimeField()