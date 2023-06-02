from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=120, unique=True)
    fio = models.CharField(max_length=120)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio', 'username']


class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    price = models.IntegerField()


class Cart(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_price = models.IntegerField(default=0)