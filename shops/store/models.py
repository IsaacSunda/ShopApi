from django.db import models
from account.models import Person, Address, Payment


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    available_quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=8, )
    imageUrl = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)


class Cart(models.Model):
    cartSession = models.CharField(max_length=200)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    cost = models.IntegerField()
    productPrice = models.DecimalField(decimal_places=2, max_digits=8,)



class Transaction(models.Model):
    ref = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=8, )
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    paymentMethod = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)


class Order(models.Model):
    shippingAddress = models.ForeignKey(Address, related_name='shipping_address',  on_delete=models.DO_NOTHING)
    billingAddress = models.ForeignKey(Address, related_name="billing_address", on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=100)
    transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING, null=True)

