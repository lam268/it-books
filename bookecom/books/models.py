from django.conf import settings
from django.db import models
from django.shortcuts import reverse

# Create your models here.

CATEGORY_CHOICES = (
    ('E', 'Equipment'),
    ('FW', 'Footwear'), 
    ('A', 'Accessories'),
    ('C', 'Clothes'),
)

class Item(models.Model):
    name = models.CharField(max_length = 200, null = True)
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    discount_price = models.FloatField(blank = True, null = True)
    category = models.CharField(choices = CATEGORY_CHOICES, max_length = 2)
    image = models.ImageField(null = True, blank = True)
    slug = models.SlugField()
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:product', kwargs= {
            'slug': self.slug,
        })

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null= True)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField()
    transaction_id = models.CharField(max_length = 200, null = True)

    def __str__(self):
        return self.user.username

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null= True)
    address= models.CharField(max_length=200, null=True)
    city = models.CharField(max_length = 200, null =True)
    date_added = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=200, null =True)
    zipcode = models.CharField(max_length=200, null =True)

    def __str__(self):
        return self.address