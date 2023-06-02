from rest_framework import serializers
from .models import User, Product, Cart, Order
from rest_framework.serializers import ModelSerializer, Serializer


class RegSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['fio', 'email', 'password']

        def save(self, **kwargs):
            user=User(
                email=self.validated_data['email'],
                fio=self.validated_data['fio'],
                username=self.validated_data['fio'],
            )
            user.set_password(self.validated_data['password'])
            user.save()
            return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'products']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

