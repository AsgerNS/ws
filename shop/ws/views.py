from django.shortcuts import render
from rest_framework.authtoken.models import Token

from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import User, Product, Cart, Order
from .serializers import RegSerializer, LoginSerializer, ProductSerializer, CartSerializer, OrderSerializer


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = User.objects.get(emai=serializer.validated_data['email'])
        except:
            return Response({
                'error': {
                    'code': 401,
                    'message': 'Authenticated failed'
                }
            })
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'data': {
                'user_token': token.key
            }
        }, status=200)
    return Response({
        'error': {
            'code': 422,
            'message': 'Validation error',
            'errors': serializer.errors
        }
    }, status=422)


@api_view(['POST'])
def signup(request):
    serializer = RegSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response ({
            'data': {
                'user_token': token.key
            }
        }, status=200)
    return Response({
        'error': {
            'code': 422,
            'message': 'Validation error',
            'errors': serializer.errors
        }
    }, status=422)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({
        'message': 'Logout'
    })


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response({
        'data': serializer.data
    }, status=200)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'data': {
                'id': serializer.data['id'],
                'message': 'Product added'
            }
        })
    return Response({
        'error': {
            'code': 422,
            'message': 'Validation error',
            'errors': serializer.errors
        }
    }, status=422)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
def change_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response({
            'error': {
                'code': 404,
                'message': 'Not found'
            }
        }, status=404)
    if request.method == 'PATCH':
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data
            }, status=200)
        return Response({
            'error': {
                'code': 422,
                'message': 'Validation error',
                'errors': serializer.errors
            }
        }, status=422)
    elif request.method == 'DELETE':
        product.delete()
        return Response({
            'data': 'Product removed'
        }, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    if request.user.is_staff:
        return Response({
            'error': {
                'code': 403,
                'message': 'Forbidden for you'
            }
        })
    cart, _ = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    data = []
    count = 0
    for p in serializer.data['products']:
        count = count + 1
        data.append({
            'id': count,
            'product_id': p['id'],
            'name': p['name'],
            'description': p['description'],
            'price': p['price']
        })
        print(data)
        return Response(data, status=200)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_cart(request, pk):
    if request.user.is_staff:
        return Response({
            'error': {
                'code': 403,
                'message': 'Forbidden for you'
            }
        })
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response({
                'error': {
                    'code': 404,
                    'message': 'Not found'
                }
            }, status=404)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)
        return Response({
            'data': {
                'message': 'Product add to cart'
            }
        }, status=201)
    elif request.method == 'DELETE':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        print(cart)
        try:
            product = cart.products.all().get(pk=pk)
        except:
            return Response({
                'error': {
                    'code': 404,
                    'message': 'Not found'
                }
            }, status=404)
        cart.products.remove(product)
        return Response({
            'data': {
                'message': 'Product removed from cart'
            }
        }, status=200)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order(request):
    if request.user.is_staff:
        return Response({
            'error': {
                'code': 403,
                'message': 'Forbidden for you'
            }
        })
    if request.method == 'GET':
        order = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(order, many=True)
        return Response({
            'data': serializer.data
        }, status=200)
    elif request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
        except:
            return Response({
                'error': {
                    'code': 422,
                    'message': 'Cart is empty'
                }
            }, status=422)
        order = Order.objects.create(user=request.user)
        total = 0
        if create_product.all().count() == 0:
            return Response({
                'error': {
                    'code': 422,
                    'message': 'Cart is empty'
                }
            }, status=422)
        for product in cart.products.all():
            total += product.price
            order.products.add(product)
            order.order_price = total
            order.save()
            cart.delete()
            serializer = OrderSerializer(order)
            return Response({
                'data': {
                    'order_id': serializer.data['id'],
                    'message': 'Order is processed'
                }
            }, status=201)