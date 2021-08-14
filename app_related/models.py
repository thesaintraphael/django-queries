from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()

class Order(models.Model):
    order_date = models.DateField()
    shipped_date = models.DateField()
    delivered_date = models.DateField()
    coupon_code = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='LineItem')

class LineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
