import traceback

from django.db import models, transaction
from polymorphic.models import PolymorphicModel
from django.conf import settings
from django.forms.models import model_to_dict
from decimal import Decimal
from datetime import datetime
from django import forms
import stripe
from django.core.mail import send_mail
from account import models as amod
#######################################################################
###   Products

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




#######################################################################
###   Orders

class Order(models.Model):
    '''An order in the system'''
    STATUS_CHOICES = (
        ( 'cart', 'Shopping Cart' ),
        ( 'payment', 'Payment Processing' ),
        ( 'sold', 'Finalized Sale' ),
    )
    order_date = models.DateTimeField(null=True, blank=True)
    name = models.TextField(blank=True, default="Shopping Cart")
    status = models.TextField(choices=STATUS_CHOICES, default='cart', db_index=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    user = models.ForeignKey('account.User', related_name='orders',  on_delete=models.CASCADE)
    # shipping information
    ship_date = models.DateTimeField(null=True, blank=True)
    ship_tracking = models.TextField(null=True, blank=True)
    ship_name = models.TextField(null=True, blank=True)
    ship_address = models.TextField(null=True, blank=True)
    ship_address2 = models.TextField(null=True, blank=True)
    ship_city = models.TextField(null=True, blank=True)
    ship_state = models.TextField(null=True, blank=True)
    ship_zip_code = models.TextField(null=True, blank=True)

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'Order {}: {}: {}'.format(self.id, self.user.get_full_name(), self.total_price)


    def active_items(self, include_tax_item=True):
        '''Returns the active items on this order'''
        if include_tax_item: return OrderItem.objects.filter(order = self.id, status = 'active')
        else: return OrderItem.objects.filter(order = self.id, status = 'active').exclude(product = None)
        # create a query object (filter to status='active')


    def get_item(self, product, create=False):
        '''Returns the OrderItem object for the given product'''
        item = OrderItem.objects.filter(order=self, product=product).first()
        if item is None and create:
            item = OrderItem.objects.create(order=self, product=product, price=product.price, quantity=0)
        elif create and item.status != 'active':
            item.status = 'active'
            item.quantity = 0
        item.recalculate()
        item.save()
        return item


    def num_items(self):
        '''Returns the number of items in the cart'''
        print(sum(self.active_items(include_tax_item=False).values_list('quantity', flat=True)))
        return sum(self.active_items(include_tax_item=False).values_list('quantity', flat=True))


    def recalculate(self):
        '''
        Recalculates the total price of the order,
        including recalculating the taxable amount.

        Saves this Order and all child OrderLine objects.
        '''
        self.total_price = 0
        if not self.active_items().filter(product = None):
            taxItem = OrderItem()
            taxItem.description = "Sales Tax"
            taxItem.price = 0
            taxItem.quantity = 1
            taxItem.extended = 0
            taxItem.order_id = self.id
            taxItem.product = None
            taxItem.save()

        for item in self.active_items(include_tax_item=False):
            item.recalculate()
            self.total_price += item.extended

        # update/create the tax order item (calculate at 7% rate)
        taxItem = self.active_items(include_tax_item=True).get(product = None)
        taxItem.price = self.total_price*7/100
        taxItem.extended = taxItem.price
        taxItem.save()

        # update the total and save
        self.total_price += round(taxItem.price,2)
        self.save()



    def finalize(self, stripe_charge_token):
        '''Runs the payment and finalizes the sale'''
        with transaction.atomic():
            # recalculate just to be sure everything is updated
            self.recalculate()

            # check that all products are available
            for item in self.active_items(include_tax_item=False):
                if item.product.__class__.__name__ == "BulkProduct" and item.quantity > item.product.Quantity:
                    raise forms.ValidationError('Sorry! An Error occurred, try again')

            # contact stripe and run the payment (using the stripe_charge_token)
            stripe.api_key = "sk_test_wadBVqwzbMzhY9jhgE5QqmJW"

            try:
                charge = stripe.Charge.create(
                    amount=round(self.total_price*100),
                    currency='usd',
                    description='Example charge',
                    source=stripe_charge_token,
                )
            except:
                traceback.print_exc()
                raise forms.ValidationError('Sorry! An Error occurred, try again')

            # finalize (or create) one or more payment objects
            NewPayment = Payment()
            NewPayment.amount = self.total_price
            NewPayment.order = self
            NewPayment.payment_date = datetime.now()
            NewPayment.save()

            # set order status to sold and save the order
            self.order_date = datetime.now()
            self.status = "sold"
            self.save()

            #add products to receipt list
            recieptlist = 'Thanks for your Order!\n\nDate: ' + str(self.order_date.date()) + '\nTotal: ' + str(self.total_price) + '\n\nShipping to: ' + str(self.ship_name) + ' ' + str(self.ship_address) + ' ' + str(self.ship_address2) + '\n' + str(self.ship_city) + ' ' + str(self.ship_state) + ' ' + str(self.ship_zip_code) + '\n\nItems:\n'
            for item in self.active_items(include_tax_item=True):
                    if item.product is not None:
                        recieptlist += str(item.quantity) +  ' ' + str(item.product.Name) + ' $' + str(item.price) +'\n'

                    else:
                        recieptlist += '\Sales Tax: $' + str(item.price)

            # update product quantities for BulkProducts
            for item in self.active_items(include_tax_item=False):
                updateproduct = item.product
                if item.product.__class__.__name__ == "BulkProduct":
                    updateproduct.Quantity -= item.quantity
                    if updateproduct.Quantity == 0: updateproduct.Status = "I"
                # update status for IndividualProducts
                else: updateproduct.Status = "I"

                updateproduct.save()

            #Send an email
            send_mail(
                'FOMO Recent Purchase',
                recieptlist,
                'OrderConfirmation@familyorientedmusic.me',
                [self.user.email],
                fail_silently=False,
            )


class OrderItem(PolymorphicModel):
    '''A line item on an order'''
    STATUS_CHOICES = (
        ( 'active', 'Active' ),
        ( 'deleted', 'Deleted' ),
    )
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    status = models.TextField(choices=STATUS_CHOICES, default='active', db_index=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    quantity = models.IntegerField(default=0)
    extended = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'OrderItem {}: {}: {}'.format(self.id, self.product.name, self.extended)


    def recalculate(self):
        '''Updates the order item's price, quantity, extended'''
        # update the price if it isn't already set and we have a product
        if self.price == 0 and self.product is not None:
            self.price = self.product.price
        # default the quantity to 1 if we don't have a quantity set
        if self.quantity == 0: self.quantity = 1

        # calculate the extended (price * quantity)
        self.extended = self.price*self.quantity

        # save the changes
        self.save()


class Payment(models.Model):
    '''A payment on a sale'''
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2) # max number is 999,999.99
    validation_code = models.TextField(null=True, blank=True)
