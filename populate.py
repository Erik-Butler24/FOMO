#!/usr/bin/env python3

# set up django first
import os, os.path
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FOMO.settings")
django.setup()
import datetime


# regular imports
from manager import models as cmod

import random
from itertools import cycle

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."



# ensure the user really wants to do this
areyousure = input('''
  You are about to drop and recreate the entire database.
  All data are about to be deleted.  Use of this script
  may cause itching, vertigo, dizziness, tingling in
  extremities, loss of balance or coordination, slurred
  speech, and driving Teslas in space.

  Please type 'yes' to confirm the data destruction: ''')
if areyousure.lower() != 'yes':
    print()
    print('  Wise choice.')
    sys.exit(1)




##################################
###   Products

cmod.ProductImage.objects.all().delete()
cmod.IndividualProduct.objects.all().delete()
cmod.RentalProduct.objects.all().delete()
cmod.BulkProduct.objects.all().delete()
cmod.Category.objects.all().delete()


# categories
print('Creating categories...')

categories = []
for catname in ( 'Instruments', 'Sheet Music', 'Electronics', 'Software', 'Lesson Books' ):
    c = cmod.Category()
    c.Name = catname
    c.Description = 'This is a category named {}'.format(catname)
    c.save()
    categories.append(c)

# products
print('Creating products...')
for i in range(1, 25):
    p = cmod.BulkProduct()
    p.Name = 'unset'  # see image adding below
    p.Description = 'unset'
    p.Category = random.choice(categories)
    p.Status = 'A'
    p.Price = random.uniform(1, 1000)
    p.ReorderTrigger = random.randint(5, 15)
    p.Quantity = random.randint(p.ReorderTrigger, 2 * p.ReorderTrigger)
    p.ReorderQuantity = p.ReorderTrigger * 2
    p.save()
for i in range(1, 25):
    p = cmod.RentalProduct()
    p.Name = 'unset'  # see image adding below
    p.Description = 'unset'
    p.Category = random.choice(categories)
    p.Status = 'A'
    p.Price = random.uniform(1, 1000)
    p.ItemID = ''.join([ random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789012345678901234567890123456789') for j in range(6) ])
    p.MaxRental = random.randint(1, 10)
    p.RetireDate = datetime.datetime.now()
    p.save()
for i in range(1, 25):
    p = cmod.IndividualProduct()
    p.Name = 'unset'  # see image adding below
    p.Description = 'unset'
    p.Category = random.choice(categories)
    p.Status = 'A'
    p.Price = random.uniform(1, 1000)
    p.ItemID = ''.join([ random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789012345678901234567890123456789') for j in range(6) ])
    p.save()


##################################
###   Product Images

print('Adding product images...')

# get a list of the product image filenames
filenames = []
for fn in os.listdir('catalog/media'):
    name, ext = os.path.splitext(fn)
    if ext.lower() == '.jpg' and name != 'notfound':
        filenames.append(fn)
random.shuffle(filenames)
images = cycle(filenames)

# add 0-4 images to each product
for product in cmod.Product.objects.all():
    for i in range(random.randint(1, 5)):
        pi = cmod.ProductImage()
        pi.filename = next(images)
        pi.product = product
        pi.save()
        if i == 0:
            name, _ = os.path.splitext(pi.filename)
            product.Name = ' '.join(( s.capitalize() for s in name.split('_') ))
            product.Description = '<p>This item is an individual product named %s.<p><p>%s</p>' % (product.Name, LOREM_IPSUM)
            product.save()

# remove the images from the first product
product = cmod.Product.objects.all().first()
for pi in product.images.all():
    pi.delete()
